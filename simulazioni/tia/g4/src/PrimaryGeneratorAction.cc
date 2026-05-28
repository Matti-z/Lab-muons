
#include "PrimaryGeneratorAction.hh"
#include "PrimaryGeneratorAction.hh"

#include "G4Event.hh"
#include "G4ParticleGun.hh"
#include "G4GeneralParticleSource.hh"

#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"

// using namespace CLHEP;  // ADD THIS LINE

#include "G4SystemOfUnits.hh"
#include "G4PhysicalConstants.hh"
#include "Randomize.hh"
#include <cmath>


PrimaryGeneratorAction::PrimaryGeneratorAction()
  : outfile(0) //Initialize the output file ()<where to write to null
{
  gun = InitializeGPS();
  
}
//forse la seguente è sbagliata, forse anche la generazione su phi segue cos^2/3
void PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent)
{
G4double theta;
    G4double phi;

    // Rejection sampling
    while(true)
    {
        theta = acos(G4UniformRand());

        G4double y = G4UniformRand();

        if(y < pow(cos(theta), 2.0/3.0))
            break;
    }

    phi = 2*pi*G4UniformRand();

    // Convert spherical -> Cartesian
    G4double dx = sin(theta)*cos(phi);
    G4double dy = sin(theta)*sin(phi);
    G4double dz = -cos(theta);

    gun->GetCurrentSource()
       ->GetAngDist()
       ->SetParticleMomentumDirection(
            G4ThreeVector(dx,dy,dz));

    gun->GeneratePrimaryVertex(anEvent);
}

PrimaryGeneratorAction::~PrimaryGeneratorAction()
{
  delete gun;
}


G4GeneralParticleSource* PrimaryGeneratorAction::InitializeGPS()
{
  G4GeneralParticleSource * gps = new G4GeneralParticleSource();
  
  // setup details easier via UI commands see gps.mac

  // particle type
  G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
  G4ParticleDefinition* muonPlus = particleTable->FindParticle("mu+");  
  G4ParticleDefinition* muonMinus = particleTable->FindParticle("mu-");  
  gps->GetCurrentSource()->SetParticleDefinition(muonMinus);

  // set energy distribution
  G4SPSEneDistribution *eneDist = gps->GetCurrentSource()->GetEneDist() ;
  eneDist->SetEnergyDisType("Gauss");
  eneDist->SetMonoEnergy(1.0*GeV);        // Mean energy (center of curve)
  eneDist->SetBeamSigmaInE(0.2*GeV);           // Standard deviation (width)

//   eneDist->SetMonoEnergy(*GeV);

  // set position distribution
  G4SPSPosDistribution *posDist = gps->GetCurrentSource()->GetPosDist();
  posDist->SetPosDisType("Plane");  // or Point,Plane,Volume,Beam
  posDist->SetCentreCoords(G4ThreeVector(0, 0, 20*cm));  // Center of plane
  posDist->SetHalfX(40*cm);   // Half-width in X direction
  posDist->SetHalfY(10*cm);   // Half-width in Y direction
  posDist->SetPosDisShape("Rectangle");  // or "Circle", "Ellipse"
  //forse per questioni geometriche sarebbe meglio fare "circle", ci proverò
//   posDist->SetCentreCoords(G4ThreeVector(0.0*cm,0.0*cm,-80.0*cm));
//   posDist->SetBeamSigmaInX(0.1*mm);
//   posDist->SetBeamSigmaInY(0.1*mm);

  // set angular distribution
  G4SPSAngDistribution *angDist = gps->GetCurrentSource()->GetAngDist();
  // angDist->SetAngDistType("cos");
  // angDist->SetParticleMomentumDirection(G4ThreeVector(0., 0.,- 1.));  // Toward -Z
//   angDist->DefineAngRefAxes("angref1",G4ThreeVector(-1.,0.,0.));

  return gps;
}
