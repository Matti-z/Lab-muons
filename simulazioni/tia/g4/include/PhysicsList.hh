
#ifndef PhysicsList_h
#define PhysicsList_h 1

#include "G4VUserPhysicsList.hh"
#include "globals.hh"


class G4VPhysicsConstructor;

class PhysicsList: public G4VUserPhysicsList
{
public:
  //! Constructor
  PhysicsList();
  //! Destructor
  ~PhysicsList();

protected:
  //! Construct particle and physics (mandatory)
  //@{
  //! Construct particles
  void ConstructParticle();
  //! Construct physics processes
  void ConstructProcess();
  //! Define user cuts
  void SetCuts();
  //@}
private:
 
  G4VPhysicsConstructor*  emPhysicsList;
 
};

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#endif