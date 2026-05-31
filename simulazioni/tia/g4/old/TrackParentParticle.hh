#ifndef TRACKPARENTPARTICLE_HH
#define TRACKPARENTPARTICLE_HH

#include "G4UnitsTable.hh"
#include "G4Types.hh"
// #include "TObject.hh"
#include "TrackParticle.hh"

class TrackParentParticle{

    public:
    TrackParentParticle();
    ~TrackParentParticle();

    
  G4int Moth_Part_ID;
  G4int Part_Type;
  G4int Moth_Part_Type;
  G4double Tot_Edep;
  G4double ZStart_Pos;
  G4double Moth_ZStart_Pos;
  G4double Moth_Tot_Edep;
  G4double Start_Time;
  G4double Moth_Start_Time;
  G4String Part_name;
  G4String Moth_Part_name;
  

  //PRESENT PARTICLE

  /// G4double TrackAddEDep(G4double e);
  /// 
  //getter
  G4int GetPart_Type() {return Part_Type;}
  float GetTot_Edep() {return Tot_Edep;}
  G4int GetMoth_Part_ID() {return Moth_Part_ID;}
  G4String GetPart_name() {return Part_name;}
  G4double GetZStart_Pos() {return ZStart_Pos;}
  G4double GetStart_Time() {return Start_Time;}


  //setter
  /// 
  /// /// void SetPart_Type(G4int ptype);
  /// /// void SetMothPart_ID(G4int mpID);
  /// /// void SetEdep(G4double ed);
  /// /// void SetPart_name(G4String pname);
  /// /// void SetZStart_Pos(G4double zstpos);
  /// /// void SetStart_Time(G4double stime);
  /// /// //void SetEnd_Pos(G4ThreeVector endpos);
  /// 
  void SetIntValues(G4int* IntArray);
  void SetDoubleValues(double* DoubleArray);

   //MOTHER PARTICLE
  /// 
  /// //getter
  /// 
  G4double GetMothTrackEDep();
  G4int GetMothPart_Type() {return Moth_Part_Type;}
  G4double GetMothTot_Edep() {return Moth_Tot_Edep;}
  G4String GetMothPart_name() {return Moth_Part_name;}
  float GetMothZStart_Pos() {return Moth_ZStart_Pos;}
  G4double GetMothStart_Time() {return Moth_Start_Time;}

   //setter
  // void SetMoth_Part_Type(G4int pptype);
  // void SetMoth_Edep(G4double ped);
  // void SetMoth_Part_name(G4String ppname);
  // void SetMoth_ZStart_Pos(G4double pzs);
  // void SetMoth_Start_Time(G4double pstime);
  // void SetEnd_Pos(G4ThreeVector endpos);

  // TrackParentParticle operator=(const TrackParentParticle &original); 
  // void* operator new(std::size_t size);

};

 #endif

}