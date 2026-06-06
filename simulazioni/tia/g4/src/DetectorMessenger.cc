#include "DetectorMessenger.hh"
#include "DetectorConstruction.hh"
#include "G4UIdirectory.hh"
#include "G4UIcmdWithADoubleAndUnit.hh"
#include "G4SystemOfUnits.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

DetectorMessenger::DetectorMessenger(DetectorConstruction* det)
 : detector(det)
{
  detDir = new G4UIdirectory("/detector/");
  detDir->SetGuidance("Detector control commands.");

  // Scintillator 1 Y-offset command
  scint1YOffsetCmd = new G4UIcmdWithADoubleAndUnit("/detector/scint1YOffset", this);
  scint1YOffsetCmd->SetGuidance("Set Y-offset for scintillator 1 (Partenope)");
  scint1YOffsetCmd->SetParameterName("offset", false);
  scint1YOffsetCmd->SetUnitCategory("Length");
  scint1YOffsetCmd->SetDefaultValue(0.0);

  // Scintillator 2 Y-offset command
  scint2YOffsetCmd = new G4UIcmdWithADoubleAndUnit("/detector/scint2YOffset", this);
  scint2YOffsetCmd->SetGuidance("Set Y-offset for scintillator 2 (Giunone)");
  scint2YOffsetCmd->SetParameterName("offset", false);
  scint2YOffsetCmd->SetUnitCategory("Length");
  scint2YOffsetCmd->SetDefaultValue(0.0);

  // Scintillator 3 Y-offset command
  scint3YOffsetCmd = new G4UIcmdWithADoubleAndUnit("/detector/scint3YOffset", this);
  scint3YOffsetCmd->SetGuidance("Set Y-offset for scintillator 3 (Minerva)");
  scint3YOffsetCmd->SetParameterName("offset", false);
  scint3YOffsetCmd->SetUnitCategory("Length");
  scint3YOffsetCmd->SetDefaultValue(0.0);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

DetectorMessenger::~DetectorMessenger()
{
  delete scint1YOffsetCmd;
  delete scint2YOffsetCmd;
  delete scint3YOffsetCmd;
  delete detDir;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void DetectorMessenger::SetNewValue(G4UIcommand* command, G4String newValue)
{
  if (command == scint1YOffsetCmd) {
    detector->SetScintillator1_YOffset(scint1YOffsetCmd->GetNewDoubleValue(newValue));
  }
  else if (command == scint2YOffsetCmd) {
    detector->SetScintillator2_YOffset(scint2YOffsetCmd->GetNewDoubleValue(newValue));
  }
  else if (command == scint3YOffsetCmd) {
    detector->SetScintillator3_YOffset(scint3YOffsetCmd->GetNewDoubleValue(newValue));
  }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
