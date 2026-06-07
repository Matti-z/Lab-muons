// il detectormessenger serve a modificare geometry del sistema
//senza cambiare il file

#ifndef DetectorMessenger_h
#define DetectorMessenger_h 1

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#include "globals.hh"
#include "G4UImessenger.hh"
#include "G4UIdirectory.hh"
#include "G4UIcmdWithADoubleAndUnit.hh"

class DetectorConstruction;
class G4UIdirectory;
class G4UIcmdWithAString;
class G4UIcmdWithADoubleAndUnit;
class G4UIcmdWith3VectorAndUnit;
class G4UIcmdWithoutParameter;
class G4UIcmdWithABool;

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

/*!
\brief This class provides the user interface to DetectorConstruction

It allows for
 - change of detector position

\sa SetNewValue()
*/
class DetectorMessenger: public G4UImessenger
{
public:
  //! Constructor
  DetectorMessenger(DetectorConstruction* det);
  //! Destructor
  ~DetectorMessenger();
    
    virtual void SetNewValue(G4UIcommand* command, G4String newValue);
  //! handle user commands
  //forse fovrei usare il seguente
//     void SetNewValue(G4UIcommand*, G4String);
    
private:
  
  DetectorConstruction*      detector;
    
  G4UIdirectory*             detDir;

    G4UIcmdWithADoubleAndUnit* scint1YOffsetCmd;
    G4UIcmdWithADoubleAndUnit* scint2YOffsetCmd;
    G4UIcmdWithADoubleAndUnit* scint3YOffsetCmd;
//       G4UIdirectory*             secondSensorDir;
//             

//       G4UIcmdWithoutParameter*   updateCmd;    
//     
//       G4UIcmdWithABool*			 setDUTsetupCmd;
};
 
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#endif

