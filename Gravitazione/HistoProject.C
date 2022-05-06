#include "TH1.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TStyle.h"
#include "TTree.h"
#include <array>


void histo() {

  gStyle->SetOptStat(2210);

// Window for Visualization 
  TCanvas* c3 = new TCanvas("c3","Time's Occourences",200,10,1100,900);
  c3->SetGridx();
  c3->SetGridy();



// TTree filled with Data on Degrees Distribution
  TTree* t8 = new TTree("t8", "tree");
  t8->ReadFile("/home/matteo/sistemi_complessi/step8.txt", "Time",' ');
  TTree* t4 = new TTree("t4", "tree");
  t4->ReadFile("/home/matteo/sistemi_complessi/step4.txt", "Time",' ');
  TTree* t2 = new TTree("t2", "tree");
  t2->ReadFile("/home/matteo/sistemi_complessi/step2.txt", "Time",' ');
  TTree* t1 = new TTree("t1", "tree");
  t1->ReadFile("/home/matteo/sistemi_complessi/step1.txt", "Time",' ');

  TH1I* h1=new TH1I("h1","Tempi maggiori di t=500",10, -0.5, 9.5);  
  TH1I* h2=new TH1I("h2","Tempi maggiori di t=500",10, -0.5, 9.5);
  TH1I* h4=new TH1I("h4","Tempi maggiori di t=500",10, -0.5, 9.5);
  TH1I* h8=new TH1I("h8","Tempi maggiori di t=500",10, -0.5, 9.5);
 
  std::vector<int> step8 = {};
  std::vector<int> step4 = {};
  std::vector<int> step2 = {};
  std::vector<int> step1 = {};

  
  int sz8 = t8->Draw("Time", "Time");
  int sz1 = t1->Draw("Time", "Time");
  int sz2 = t2->Draw("Time", "Time");
  int sz4 = t4->Draw("Time", "Time");
  Double_t *v8 = t8->GetV1();
  Double_t *v4 = t4->GetV1();
  Double_t *v2 = t2->GetV1();
  Double_t *v1 = t1->GetV1();

  for ( int i = 0; i < sz8; ++i ) {
    std::cout << v8[i] << endl; 
    if (v8[i] > 500) {
    	step8.push_back(v8[i]);
    }
  }
    for ( int i = 0; i < sz4; ++i ) {
    std::cout << v4[i] << endl; 
    if (v4[i] > 500) {
    	step4.push_back(v4[i]);
    }
  }
    for ( int i = 0; i < sz2; ++i ) {
    std::cout << v2[i] << endl; 
    if (v2[i] > 500) {
    	step2.push_back(v2[i]);
    }
  }
    for ( int i = 0; i < sz1; ++i ) {
    std::cout << v1[i] << endl; 
    if (v1[i] > 500) {
    	step1.push_back(v1[i]);
    }
  }
  std::cout << "Actual elements in d8: " << step8.size() << endl;
  std::cout << "Actual elements in d4: " << step4.size() << endl;
  std::cout << "Actual elements in d2: " << step2.size() << endl;
  std::cout << "Actual elements in d1: " << step1.size() << endl;


   for(int j = 0; j < step8.size(); j++) {
   	h8->Fill(8);
   }
   for(int j = 0; j < step4.size(); j++) {
   	h4->Fill(4);
   }
   for(int j = 0; j < step2.size(); j++) {
   	h2->Fill(2);
   }
   for(int j = 0; j < step1.size(); j++) {
   	h1->Fill(1);
   }

// Cosmetics
  h1->SetTitleSize(1.5);
  h1->SetFillColor(38);
  h1->SetLineColor(kBlue+2);
  h1->SetLineWidth(2);
  h1->GetXaxis()->SetTitle("Distanza di influenza");
  h1->GetXaxis()->SetTitleSize(0.04);
  h1->GetYaxis()->SetTitle("Occorrenze");
  h1->GetYaxis()->SetTitleSize(0.04);
  h1->Draw();
  
  h8->SetTitleSize(1.5);
  h8->SetFillColor(46);
  h8->SetLineColor(kBlue+2);
  h8->SetLineWidth(2);
  h8->GetXaxis()->SetTitle("Distance");
  h8->GetXaxis()->SetTitleSize(0.04);
  h8->GetYaxis()->SetTitle("Occourences");
  h8->GetYaxis()->SetTitleSize(0.04);
  h8->Draw("SAME");
  
  h4->SetTitleSize(1.5);
  h4->SetFillColor(kOrange);
  h4->SetLineColor(kBlue+2);
  h4->SetLineWidth(2);
  h4->GetXaxis()->SetTitle("Distance");
  h4->GetXaxis()->SetTitleSize(0.04);
  h4->GetYaxis()->SetTitle("Occourences");
  h4->GetYaxis()->SetTitleSize(0.04);
  h4->Draw("SAME");
  
  h2->SetTitleSize(1.5);
  h2->SetFillColor(8);
  h2->SetLineColor(kBlack);
  h2->SetLineWidth(2);
  h2->GetXaxis()->SetTitle("Distance");
  h2->GetXaxis()->SetTitleSize(0.04);
  h2->GetYaxis()->SetTitle("Occourences");
  h2->GetYaxis()->SetTitleSize(0.04);
  h2->Draw("SAME");
  
  gStyle->SetOptStat(0);
  
  c3->SaveAs("Time_distribution_correlation.pdf");


}

