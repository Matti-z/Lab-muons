#include "StackingAction.hh"
#include "G4ClassificationOfNewTrack.hh"
#include "G4Track.hh"
#include "G4Gamma.hh"
#include "G4Neutron.hh"
//#include "G4TrackStatus.hh"
//#include "G4ParticleDefinition.hh"
//#include "G4ParticleTypes.hh"
//#include "G4TouchableHistory.hh"
//#include "G4VPhysicalVolume.hh"
//#include "G4VProcess.hh"
//#include <iostream>
//#include <string>
//#include <cmath>


StackingAction::StackingAction():
  old_TrackID(-1)
{
}


StackingAction::~StackingAction() {
}


G4ClassificationOfNewTrack 
StackingAction::ClassifyNewTrack( const G4Track * aTrack ) 
{
  
  
  //At the beginning all the tracks are urgent
  G4ClassificationOfNewTrack result( fUrgent );
  

  //I want to get the number of the previous track
  old_TrackID = aTrack->GetParentID();

  //If the previous track came "before" this track,
  //the present track is put on Waiting State
  //The waiting stack is processed after the urgent stack is finished
  if ( aTrack->GetTrackID() > old_TrackID )//This is a secondary
    {
      result = fWaiting;
    }
  
  else 
    {
      result = fUrgent;
    }
  

  return result;
  
}


