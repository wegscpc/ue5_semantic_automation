// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Sockets.h"
#include "SocketSubsystem.h"
#include "Interfaces/IPv4/IPv4Address.h"
#include "Interfaces/IPv4/IPv4Endpoint.h"
#include "HAL/Runnable.h"
#include "HAL/RunnableThread.h"
#include "PythonBridge.generated.h"

/**
 * TCP Bridge for communicating with Python backend
 * Handles socket communication, command serialization, and response parsing
 */
UCLASS()
class UE5SEMANTICAUTOMATION_API UPythonBridge : public UObject, public FRunnable
{
	GENERATED_BODY()

public:
	UPythonBridge();
	virtual ~UPythonBridge();

	/**
	 * Initialize the bridge and start listening for connections
	 * @param Port - Port to listen on (default: 55557)
	 * @return true if initialization succeeded
	 */
	UFUNCTION(BlueprintCallable, Category = "Python Bridge")
	bool Initialize(int32 Port = 55557);

	/**
	 * Shutdown the bridge and close all connections
	 */
	UFUNCTION(BlueprintCallable, Category = "Python Bridge")
	void Shutdown();

	/**
	 * Send a command to the Python backend
	 * @param Command - Command name
	 * @param Params - JSON parameters
	 * @return Response from Python as JSON string
	 */
	UFUNCTION(BlueprintCallable, Category = "Python Bridge")
	FString SendCommand(const FString& Command, const FString& Params);

	/**
	 * Check if the bridge is connected to Python backend
	 */
	UFUNCTION(BlueprintCallable, Category = "Python Bridge")
	bool IsConnected() const { return bIsConnected; }

	// FRunnable interface
	virtual bool Init() override;
	virtual uint32 Run() override;
	virtual void Stop() override;
	virtual void Exit() override;

private:
	/** Socket for listening to incoming connections */
	FSocket* ListenerSocket;

	/** Active client socket */
	FSocket* ClientSocket;

	/** Thread for running the socket listener */
	FRunnableThread* Thread;

	/** Port to listen on */
	int32 ListenPort;

	/** Whether the bridge is connected */
	bool bIsConnected;

	/** Whether the thread should continue running */
	bool bShouldRun;

	/** Critical section for thread safety */
	FCriticalSection CriticalSection;

	/**
	 * Accept incoming connections
	 */
	void AcceptConnection();

	/**
	 * Receive data from the client socket
	 */
	FString ReceiveData();

	/**
	 * Send data to the client socket
	 */
	bool SendData(const FString& Data);
};
