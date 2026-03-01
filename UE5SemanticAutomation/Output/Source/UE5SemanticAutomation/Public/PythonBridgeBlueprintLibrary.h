// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "PythonBridgeBlueprintLibrary.generated.h"

/**
 * Blueprint Function Library for Python Bridge Communication
 * Provides easy-to-use Blueprint nodes for sending commands to the Python bridge
 */
UCLASS()
class UE5SEMANTICAUTOMATION_API UPythonBridgeBlueprintLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	/**
	 * Send a command to the Python bridge server
	 * @param Command - The command name (e.g., "suggest_name", "ping")
	 * @param Params - JSON string with command parameters
	 * @param Response - Output response from the server
	 * @return True if command was sent successfully
	 */
	UFUNCTION(BlueprintCallable, Category = "Python Bridge")
	static bool SendCommandToBridge(const FString& Command, const FString& Params, FString& Response);

	/**
	 * Suggest a name for an asset using AI
	 * @param OriginalName - The original asset name
	 * @param AssetType - The type of asset (e.g., "StaticMesh", "Texture2D")
	 * @param SuggestedName - Output suggested name
	 * @return True if successful
	 */
	UFUNCTION(BlueprintCallable, Category = "Python Bridge|AI")
	static bool SuggestAssetName(const FString& OriginalName, const FString& AssetType, FString& SuggestedName);

	/**
	 * Generate material parameters from description
	 * @param Description - Material description (e.g., "shiny red metal")
	 * @param MaterialParams - Output JSON string with material parameters
	 * @return True if successful
	 */
	UFUNCTION(BlueprintCallable, Category = "Python Bridge|Materials")
	static bool GenerateMaterial(const FString& Description, FString& MaterialParams);

	/**
	 * Generate metadata for an asset
	 * @param AssetName - The asset name
	 * @param AssetType - The asset type
	 * @param Metadata - Output JSON string with metadata
	 * @return True if successful
	 */
	UFUNCTION(BlueprintCallable, Category = "Python Bridge|Metadata")
	static bool GenerateMetadata(const FString& AssetName, const FString& AssetType, FString& Metadata);

	/**
	 * Ping the Python bridge to check if it's running
	 * @return True if bridge is responding
	 */
	UFUNCTION(BlueprintCallable, Category = "Python Bridge")
	static bool PingBridge();

	/**
	 * Check if the Python bridge is connected
	 * @return True if connected
	 */
	UFUNCTION(BlueprintPure, Category = "Python Bridge")
	static bool IsBridgeConnected();
};
