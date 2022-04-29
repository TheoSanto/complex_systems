#include "TH1.h"
#include "TRandom.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TStyle.h"
#include "TTree.h"
#include <array>

void opinions_histos() {

  gStyle->SetOptStat(2210);
  //gStyle->SetOptFit(111);

// Window for Visualization of Initial Opinions' Distribution
  TCanvas* c1 = new TCanvas("c1","Initial Opinions' Distribution",200,10,1100,900);
  c1->SetGridx();
  c1->SetGridy();

// TTree filled with Data on Initial Opinions' Distribution
  TTree* t_in = new TTree("t_in", "tree from data_in.csv");
  t_in->ReadFile("data_in.csv", "Class/C:ID/D:Opinion:Position:Time_Step", ',');

// Histogram filled with Opinion Data of  TTree 't_in'
  TH1F* h_in=new TH1F("h_in","Initial Opinions' Distribution",16, -1.1, 1.1);  
  t_in->Draw("Opinion>>h_in");
  h_in->SetBinContent(0,0);
  h_in->ResetStats();

// Histogram 'h_in' Cosmetics
  h_in->SetTitleSize(1.5);
  h_in->SetFillColor(kBlue);
  h_in->SetLineColor(kBlue+2);
  h_in->SetLineWidth(2);
  h_in->GetXaxis()->SetTitle("Opinion Parameter");
  h_in->GetXaxis()->SetTitleSize(0.04);
  h_in->GetYaxis()->SetTitle("Counts");
  h_in->GetYaxis()->SetTitleSize(0.04);

// Window for Visualization of Final Opinions' Distribution
  TCanvas* c2 = new TCanvas("c2","Final Opinions' Distribution",200,10,1100,900);
  c2->SetGridx();
  c2->SetGridy();

// TTree filled with Data on Final Opinions' Distribution
  TTree* t_fin = new TTree("t_fin", "tree from /home/theo/bazzani/data_fin.csv");
  t_fin->ReadFile("/home/theo/bazzani/data_fin.csv", "Class/C:ID/D:Opinion:Position:Time_Step", ',');

// Histogram filled with Opinion Data of TTree 't_fin'
  TH1F* h_fin=new TH1F("h_fin","Final Opinions' Distribution",16, -1.1, 1.1);  
  t_fin->Draw("Opinion>>h_fin");
  h_fin->SetBinContent(0,0);
  h_fin->ResetStats();

// Histogram 'h_fin' Cosmetics
  h_fin->SetTitleSize(1.5);
  h_fin->SetFillColor(kBlue);
  h_fin->SetLineColor(kBlue+2);
  h_fin->SetLineWidth(2);
  h_fin->GetXaxis()->SetTitle("Opinion Parameter");
  h_fin->GetXaxis()->SetTitleSize(0.04);
  h_fin->GetYaxis()->SetTitle("Counts");
  h_fin->GetYaxis()->SetTitleSize(0.04);

}

void degree_histo() {

  gStyle->SetOptStat(2210);

// Window for Visualization 
  TCanvas* c3 = new TCanvas("c3","Degree of nodes' Occourences",200,10,1100,900);
  c3->SetGridx();
  c3->SetGridy();



// TTree filled with Data on Degrees Distribution
  TTree* t_deg1 = new TTree("t_deg", "tree from /home/theo/bazzani/deg.csv");
  t_deg1->ReadFile("/home/theo/bazzani/deg.csv", "Degree:Number_of_nodes", ';');
  TTree* t_deg2 = new TTree("t_deg", "tree from /home/theo/bazzani/deg.csv");
  t_deg2->ReadFile("/home/theo/bazzani/deg.csv", "Number_of_nodes:Degree", ';');
 
  TH1I* h_deg=new TH1I("h_deg","Degree of nodes' Occourences",11, -0.5, 10.5);  

  int sz1 = t_deg1->Draw("Degree", "Number_of_nodes");
  Double_t *v1 = t_deg1->GetV1();
  for ( int i = 0; i < sz1; ++i ) {
    std::cout << v1[i] << endl;
  }
  int sz2 = t_deg2->Draw("Degree", "Number_of_nodes");
  Double_t *v2 = t_deg2->GetV1();
  for ( int i = 0; i < sz2; ++i ) {
    std::cout << v2[i] << endl;
  }



  
  //TFile *file = new TFile("deg.root", "READ"); 
  //TTree * Tout= (TTree*)file->Get(0);
  //Tout->Print();

  //TFile *f = TFile::Open("deg.root");
  //TTree *t4 = (TTree *) f->GetObject("t0");
  //t4->Print();


//  std::array<int, 8> col1 = {0,3,4,5,6,5,3,1};
//  std::array<int, 8> col2 = {1,2,3,4,5,6,7,8};
  for(int i = 0; i <= sz1; i++) {
    for(int j = 0; j < v2[i]; j++) {
      //std::cout<<"valore "<<col1[i]<<'\n';
      //std::cout<<"indice"<<i<<'\n';
      h_deg->Fill(v1[i]);
    }
  }








  //t->ReadFile("ytt_yt.csv", "yt0_X/D:yt0_Y:yt3_X:yt3_Y:yt1_X:yt1_Y:yt2_X:yt2_Y");
  //t->Draw("yt3_Y : yt3_X");

// Histogram filled with Degree Data of TTree 't_in'

  //t_deg->Draw("Degree>>h_deg");
  //h_deg->SetBinContent(0,0);
  //h_deg->ResetStats();

// Cosmetics
  h_deg->SetTitleSize(1.5);
  h_deg->SetFillColor(kBlue);
  h_deg->SetLineColor(kBlue+2);
  h_deg->SetLineWidth(2);
  h_deg->GetXaxis()->SetTitle("Degree");
  h_deg->GetXaxis()->SetTitleSize(0.04);
  h_deg->GetYaxis()->SetTitle("Occourences");
  h_deg->GetYaxis()->SetTitleSize(0.04);
  h_deg->Draw();
  c3->SaveAs("canvas.pdf");


}

/*
col1 = [,,,,]
col2 = [,,,,,]
for j (0, i < , ++j)
    for i in range (col2[j])
        h_deg->Fill(col1[j])
        */