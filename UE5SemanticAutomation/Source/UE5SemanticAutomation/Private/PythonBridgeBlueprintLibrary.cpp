// Copyright Epic Games, Inc. All Rights Reserved.

#include "PythonBridgeBlueprintLibrary.h"
#include "PythonBridge.h"
#include "Sockets.h"
#include "SocketSubsystem.h"
#include "Json.h"
#include "JsonUtilities.h"

bool UPythonBridgeBlueprintLibrary::SendCommandToBridge(const FString& Command, const FString& Params, FString& Response)
{
	// Get socket subsystem
	ISocketSubsystem* SocketSubsystem = ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM);
	if (!SocketSubsystem)
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to get socket subsystem"));
		return false;
	}

	// Create socket
	FSocket* Socket = SocketSubsystem->CreateSocket(NAME_Stream, TEXT("PythonBridgeClient"), false);
	if (!Socket)
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to create socket"));
		return false;
	}

	// Connect to bridge
	TSharedRef<FInternetAddr> Addr = SocketSubsystem->CreateInternetAddr();
	bool bIsValid;
	Addr->SetIp(TEXT("127.0.0.1"), bIsValid);
	Addr->SetPort(55557);

	if (!bIsValid)
	{
		UE_LOG(LogTemp, Error, TEXT("Invalid IP address"));
		Socket->Close();
		SocketSubsystem->DestroySocket(Socket);
		return false;
	}

	if (!Socket->Connect(*Addr))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to connect to Python bridge on port 55557"));
		Socket->Close();
		SocketSubsystem->DestroySocket(Socket);
		return false;
	}

	// Build JSON command
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("command"), Command);

	// Parse params as JSON
	TSharedPtr<FJsonObject> ParamsObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Params);
	if (FJsonSerializer::Deserialize(Reader, ParamsObject) && ParamsObject.IsValid())
	{
		JsonObject->SetObjectField(TEXT("params"), ParamsObject);
	}
	else
	{
		// If params is not valid JSON, create empty params object
		JsonObject->SetObjectField(TEXT("params"), MakeShareable(new FJsonObject));
	}

	// Serialize to string
	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	// Send command
	int32 BytesSent = 0;
	if (!Socket->Send((uint8*)TCHAR_TO_UTF8(*JsonString), JsonString.Len(), BytesSent))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to send command to Python bridge"));
		Socket->Close();
		SocketSubsystem->DestroySocket(Socket);
		return false;
	}

	// Receive response
	uint8 Buffer[4096];
	int32 BytesRead = 0;
	if (Socket->Recv(Buffer, sizeof(Buffer) - 1, BytesRead))
	{
		Buffer[BytesRead] = '\0';
		Response = FString(UTF8_TO_TCHAR(Buffer));
		UE_LOG(LogTemp, Log, TEXT("Received response: %s"), *Response);
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to receive response from Python bridge"));
		Socket->Close();
		SocketSubsystem->DestroySocket(Socket);
		return false;
	}

	// Clean up
	Socket->Close();
	SocketSubsystem->DestroySocket(Socket);

	return true;
}

bool UPythonBridgeBlueprintLibrary::SuggestAssetName(const FString& OriginalName, const FString& AssetType, FString& SuggestedName)
{
	// Build params JSON
	FString Params = FString::Printf(TEXT("{\"original_name\":\"%s\",\"asset_type\":\"%s\"}"), *OriginalName, *AssetType);

	// Send command
	FString Response;
	if (!SendCommandToBridge(TEXT("suggest_name"), Params, Response))
	{
		return false;
	}

	// Parse response
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Response);
	if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
	{
		if (JsonObject->GetBoolField(TEXT("success")))
		{
			TSharedPtr<FJsonObject> Result = JsonObject->GetObjectField(TEXT("result"));
			SuggestedName = Result->GetStringField(TEXT("suggested_name"));
			return true;
		}
		else
		{
			FString Error = JsonObject->GetStringField(TEXT("error"));
			UE_LOG(LogTemp, Error, TEXT("Python bridge error: %s"), *Error);
			return false;
		}
	}

	return false;
}

bool UPythonBridgeBlueprintLibrary::GenerateMaterial(const FString& Description, FString& MaterialParams)
{
	FString Params = FString::Printf(TEXT("{\"description\":\"%s\"}"), *Description);
	FString Response;
	
	if (!SendCommandToBridge(TEXT("generate_material"), Params, Response))
	{
		return false;
	}

	MaterialParams = Response;
	return true;
}

bool UPythonBridgeBlueprintLibrary::GenerateMetadata(const FString& AssetName, const FString& AssetType, FString& Metadata)
{
	FString Params = FString::Printf(TEXT("{\"asset_name\":\"%s\",\"asset_type\":\"%s\"}"), *AssetName, *AssetType);
	FString Response;
	
	if (!SendCommandToBridge(TEXT("generate_metadata"), Params, Response))
	{
		return false;
	}

	Metadata = Response;
	return true;
}

bool UPythonBridgeBlueprintLibrary::PingBridge()
{
	FString Response;
	return SendCommandToBridge(TEXT("ping"), TEXT("{}"), Response);
}

bool UPythonBridgeBlueprintLibrary::IsBridgeConnected()
{
	return PingBridge();
}
