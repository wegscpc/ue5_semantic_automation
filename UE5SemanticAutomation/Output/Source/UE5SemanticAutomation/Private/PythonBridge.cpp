// Copyright Epic Games, Inc. All Rights Reserved.

#include "PythonBridge.h"
#include "Sockets.h"
#include "SocketSubsystem.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonWriter.h"
#include "Dom/JsonObject.h"

UPythonBridge::UPythonBridge()
	: ListenerSocket(nullptr)
	, ClientSocket(nullptr)
	, Thread(nullptr)
	, ListenPort(55557)
	, bIsConnected(false)
	, bShouldRun(false)
{
}

UPythonBridge::~UPythonBridge()
{
	Shutdown();
}

bool UPythonBridge::Initialize(int32 Port)
{
	ListenPort = Port;

	// Get socket subsystem
	ISocketSubsystem* SocketSubsystem = ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM);
	if (!SocketSubsystem)
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to get socket subsystem"));
		return false;
	}

	// Create listener socket
	ListenerSocket = SocketSubsystem->CreateSocket(NAME_Stream, TEXT("PythonBridge Listener"), false);
	if (!ListenerSocket)
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to create listener socket"));
		return false;
	}

	// Set socket options
	ListenerSocket->SetReuseAddr(true);
	ListenerSocket->SetNonBlocking(true);

	// Bind to port
	TSharedRef<FInternetAddr> Addr = SocketSubsystem->CreateInternetAddr();
	Addr->SetAnyAddress();
	Addr->SetPort(ListenPort);

	if (!ListenerSocket->Bind(*Addr))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to bind socket to port %d"), ListenPort);
		return false;
	}

	// Start listening
	if (!ListenerSocket->Listen(1))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to listen on socket"));
		return false;
	}

	// Start listener thread
	bShouldRun = true;
	Thread = FRunnableThread::Create(this, TEXT("PythonBridgeThread"), 0, TPri_Normal);

	UE_LOG(LogTemp, Log, TEXT("Python Bridge listening on port %d"), ListenPort);
	return true;
}

void UPythonBridge::Shutdown()
{
	bShouldRun = false;

	// Wait for thread to finish
	if (Thread)
	{
		Thread->WaitForCompletion();
		delete Thread;
		Thread = nullptr;
	}

	// Close sockets
	if (ClientSocket)
	{
		ClientSocket->Close();
		ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(ClientSocket);
		ClientSocket = nullptr;
	}

	if (ListenerSocket)
	{
		ListenerSocket->Close();
		ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(ListenerSocket);
		ListenerSocket = nullptr;
	}

	bIsConnected = false;
	UE_LOG(LogTemp, Log, TEXT("Python Bridge shutdown"));
}

FString UPythonBridge::SendCommand(const FString& Command, const FString& Params)
{
	if (!bIsConnected || !ClientSocket)
	{
		UE_LOG(LogTemp, Warning, TEXT("Python Bridge not connected"));
		return TEXT("{\"error\": \"Not connected\"}");
	}

	// Create JSON command
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("command"), Command);
	
	// Parse params as JSON
	TSharedPtr<FJsonObject> ParamsObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Params);
	if (FJsonSerializer::Deserialize(Reader, ParamsObject) && ParamsObject.IsValid())
	{
		JsonObject->SetObjectField(TEXT("params"), ParamsObject);
	}

	// Serialize to string
	FString OutputString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&OutputString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	// Send command
	if (!SendData(OutputString))
	{
		return TEXT("{\"error\": \"Failed to send command\"}");
	}

	// Receive response
	FString Response = ReceiveData();
	return Response;
}

bool UPythonBridge::Init()
{
	return true;
}

uint32 UPythonBridge::Run()
{
	while (bShouldRun)
	{
		AcceptConnection();
		FPlatformProcess::Sleep(0.1f);
	}
	return 0;
}

void UPythonBridge::Stop()
{
	bShouldRun = false;
}

void UPythonBridge::Exit()
{
}

void UPythonBridge::AcceptConnection()
{
	if (!ListenerSocket)
		return;

	bool bHasPendingConnection = false;
	if (ListenerSocket->HasPendingConnection(bHasPendingConnection) && bHasPendingConnection)
	{
		FScopeLock Lock(&CriticalSection);

		// Close existing connection
		if (ClientSocket)
		{
			ClientSocket->Close();
			ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(ClientSocket);
		}

		// Accept new connection
		ClientSocket = ListenerSocket->Accept(TEXT("PythonBridge Client"));
		if (ClientSocket)
		{
			bIsConnected = true;
			UE_LOG(LogTemp, Log, TEXT("Python client connected"));
		}
	}
}

FString UPythonBridge::ReceiveData()
{
	if (!ClientSocket)
		return TEXT("");

	FScopeLock Lock(&CriticalSection);

	uint32 PendingDataSize = 0;
	if (!ClientSocket->HasPendingData(PendingDataSize))
		return TEXT("");

	TArray<uint8> ReceivedData;
	ReceivedData.SetNumUninitialized(PendingDataSize);

	int32 BytesRead = 0;
	if (!ClientSocket->Recv(ReceivedData.GetData(), ReceivedData.Num(), BytesRead))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to receive data"));
		return TEXT("");
	}

	FString ReceivedString = FString(UTF8_TO_TCHAR(ReceivedData.GetData()));
	return ReceivedString;
}

bool UPythonBridge::SendData(const FString& Data)
{
	if (!ClientSocket)
		return false;

	FScopeLock Lock(&CriticalSection);

	FTCHARToUTF8 Convert(*Data);
	int32 BytesSent = 0;
	
	if (!ClientSocket->Send((uint8*)Convert.Get(), Convert.Length(), BytesSent))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to send data"));
		return false;
	}

	return BytesSent == Convert.Length();
}
