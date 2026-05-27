
#include "globals.hh"
#include "PhysicsList.hh"

#include "G4EmStandardPhysics.hh"
#include "G4LossTableManager.hh"

#include "G4ProcessManager.hh"
#include "G4ParticleTypes.hh"

#include "G4SystemOfUnits.hh"
#include "G4PhysicalConstants.hh"

PhysicsList::PhysicsList():  G4VUserPhysicsList()
{
  defaultCutValue = 10.0*um;
  SetVerboseLevel(1);
  emPhysicsList = new G4EmStandardPhysics();
}

PhysicsList::~PhysicsList()
{}

void PhysicsList::ConstructParticle()
{
  // In this method, static member functions should be called
  // for all particles which you want to use.
  // This ensures that objects of these particle types will be
  // created in the program. 

  // pseudo-particles
  G4Geantino::GeantinoDefinition();
  G4ChargedGeantino::ChargedGeantinoDefinition();

  // define gamma, e+, e- and some charged Hadrons
  emPhysicsList->ConstructParticle();

  
// gamma
  G4Gamma::Gamma();

// leptons
  G4Electron::Electron();
  G4Positron::Positron();

  G4MuonPlus::MuonPlus();
  G4MuonMinus::MuonMinus();


  // mesons
//    G4PionPlus::PionPlusDefinition();
//    G4PionMinus::PionMinusDefinition();

}

void PhysicsList::ConstructProcess()
{
  AddTransportation();
  emPhysicsList->ConstructProcess();
}

void PhysicsList::SetCuts()
{
  //G4VUserPhysicsList::SetCutsWithDefault method sets 
  //the default cut value for all particle types 
  //
  SetCutsWithDefault();
     
  if (verboseLevel>0) DumpCutValuesTable();
}