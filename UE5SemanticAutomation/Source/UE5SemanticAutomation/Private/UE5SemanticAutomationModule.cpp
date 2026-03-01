// Copyright Epic Games, Inc. All Rights Reserved.

#include "UE5SemanticAutomationModule.h"
#include "PythonBridge.h"
#include "LevelEditor.h"
#include "Widgets/Docking/SDockTab.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/Text/STextBlock.h"
#include "ToolMenus.h"
#include "Framework/MultiBox/MultiBoxBuilder.h"

static const FName UE5SemanticAutomationTabName("UE5SemanticAutomation");

#define LOCTEXT_NAMESPACE "FUE5SemanticAutomationModule"

void FUE5SemanticAutomationModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
	
	UE_LOG(LogTemp, Log, TEXT("UE5 Semantic Automation Plugin Started"));

	// Initialize Python Bridge
	UPythonBridge* Bridge = NewObject<UPythonBridge>();
	if (Bridge)
	{
		if (Bridge->Initialize(55557))
		{
			UE_LOG(LogTemp, Log, TEXT("Python Bridge initialized on port 55557"));
		}
		else
		{
			UE_LOG(LogTemp, Error, TEXT("Failed to initialize Python Bridge"));
		}
	}

	// Register menus
	UToolMenus::RegisterStartupCallback(FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FUE5SemanticAutomationModule::RegisterMenus));
}

void FUE5SemanticAutomationModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.
	
	UE_LOG(LogTemp, Log, TEXT("UE5 Semantic Automation Plugin Shutdown"));

	UToolMenus::UnRegisterStartupCallback(this);
	UToolMenus::UnregisterOwner(this);
}

void FUE5SemanticAutomationModule::PluginButtonClicked()
{
	// TODO: Open main Editor Utility Widget
	UE_LOG(LogTemp, Log, TEXT("UE5 Semantic Automation button clicked"));
}

void FUE5SemanticAutomationModule::RegisterMenus()
{
	// Owner will be used for cleanup in call to UToolMenus::UnregisterOwner
	FToolMenuOwnerScoped OwnerScoped(this);

	{
		UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
		{
			FToolMenuSection& Section = Menu->FindOrAddSection("WindowLayout");
			Section.AddMenuEntry(
				FName("UE5SemanticAutomation"),
				LOCTEXT("UE5SemanticAutomation", "UE5 Semantic Automation"),
				LOCTEXT("UE5SemanticAutomationTooltip", "Open UE5 Semantic Automation Tools"),
				FSlateIcon(),
				FUIAction(FExecuteAction::CreateRaw(this, &FUE5SemanticAutomationModule::PluginButtonClicked))
			);
		}
	}

	{
		UToolMenu* ToolbarMenu = UToolMenus::Get()->ExtendMenu("LevelEditor.LevelEditorToolBar.PlayToolBar");
		{
			FToolMenuSection& Section = ToolbarMenu->FindOrAddSection("PluginTools");
			FToolMenuEntry& Entry = Section.AddEntry(FToolMenuEntry::InitToolBarButton(
				FName("UE5SemanticAutomation"),
				FUIAction(FExecuteAction::CreateRaw(this, &FUE5SemanticAutomationModule::PluginButtonClicked)),
				LOCTEXT("UE5SemanticAutomation", "Semantic Automation"),
				LOCTEXT("UE5SemanticAutomationTooltip", "Open UE5 Semantic Automation Tools"),
				FSlateIcon()
			));
		}
	}
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FUE5SemanticAutomationModule, UE5SemanticAutomation)
