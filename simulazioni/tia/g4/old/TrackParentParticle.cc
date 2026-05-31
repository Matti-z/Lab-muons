 

#include "TrackParentParticle.hh"
#include "EventAction.hh"
#include "RunAction.hh"
#include "ScintillatorSD.hh"


TrackParentParticle::TrackParentParticle(){
    Moth_Part_ID = 0;
  Part_Type = 0;
  Moth_Part_Type = 0;
  Tot_Edep = 0.0;
  ZStart_Pos = 0.0;

  bool printvalues = false;
    
  if(printvalues)
    {

      G4cout << "Creating TrackParentParticleObject" << G4endl;
      
      Moth_ZStart_Pos = 0.0;
      
      G4cout << "Initial Values \n" << G4endl;
      
      /// 
      G4cout << "MothPartID= " << Moth_Part_ID 
	     << "\t Part_Type= " << Part_Type 
	     << "\t  Moth_Part_Type= " << Moth_Part_Type
	     << "\t  Tot_Edep= " << Tot_Edep
	     << "\t  ZStart_Pos= " <<  ZStart_Pos
	     << "\t  Moth ZStart_Pos= " <<  Moth_ZStart_Pos
	     << "\t  ADDRESS of Moth ZStart_Pos= " <<  &Moth_ZStart_Pos
	     << G4endl;
      G4cout << "\n" << G4endl;
    }
  
}

TrackParentParticle::~TrackParentParticle()
{
  bool printvalues = false;
    
  if(printvalues)  G4cout << "Deleting TrackParentParticle Object" << G4endl;;
}


void TrackParentParticle::SetIntValues(G4int* IntArray)
{
  Moth_Part_ID = IntArray[0];
  
  Part_Type = IntArray[1];
  

  Moth_Part_Type = IntArray[2];
  

  bool printvalues = false;

  if(printvalues)
    {
      G4cout << "Mother Particle ID " << Moth_Part_ID << " set " << G4endl;
      G4cout << "Particle Type " << Part_Type << " set " << G4endl;
      G4cout << "Mother Particle Type " << Moth_Part_Type << " set " << G4endl;
    }
  return;
}

void TrackParentParticle::SetDoubleValues(G4double* DoubleArray)
{
  Tot_Edep = DoubleArray[0];
  
  Moth_Tot_Edep = DoubleArray[1];
  
  ZStart_Pos = DoubleArray[2];
  
  Moth_ZStart_Pos = DoubleArray[3];
      
  Start_Time = DoubleArray[4];
  
  Moth_Start_Time = DoubleArray[5];
    
  bool printvalues = false;

  if(printvalues)
    {
      G4cout << "Particle Edep " << G4BestUnit(Tot_Edep,"Energy") 
	     << " set " << G4endl;
      G4cout << "Mother Particle Edep " << G4BestUnit(Moth_Tot_Edep,"Energy") 
	     << " set " << G4endl;
      G4cout << "Particle Z Start Position " << G4BestUnit(ZStart_Pos,"Length") 
	     << " set " << G4endl;
      G4cout << "Mother Particle Z Start Position " << G4BestUnit(Moth_ZStart_Pos,"Length") 
	     << " set " << G4endl;
      G4cout << "Particle Start Time " << G4BestUnit(Start_Time,"Time") 
	     << " set " << G4endl;
      G4cout << "Mother Particle Start Time " 
	     << G4BestUnit(Moth_Start_Time,"Time") << " set " << G4endl;
    }
    
  return;
}