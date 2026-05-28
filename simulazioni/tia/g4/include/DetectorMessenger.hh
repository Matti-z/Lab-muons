// il detectormessenger serve a modificare geometry del sistema
//senza cambiare il file

#ifndef DetectorMessenger_h
#define DetectorMessenger_h 1

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#include "globals.hh"
#include "G4UImessenger.hh"

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
  DetectorMessenger(DetectorConstruction* );
  //! Destructor
  ~DetectorMessenger();
    
  //! handle user commands
  //forse fovrei usare il seguente
//     void SetNewValue(G4UIcommand*, G4String);
    
private:
  
  DetectorConstruction*      detector;
    
  G4UIdirectory*             detDir;
//       G4UIdirectory*             secondSensorDir;
//             
//       G4UIcmdWithADoubleAndUnit* xShiftCmd;    
//       G4UIcmdWithADoubleAndUnit* yShiftCmd;    
//       G4UIcmdWithADoubleAndUnit* thetaCmd;    
//     
//       G4UIcmdWithoutParameter*   updateCmd;    
//     
//       G4UIcmdWithABool*			 setDUTsetupCmd;
};
 
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#endif

