#include "TH1.h"
#include "TRandom.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TStyle.h"
#include "TTree.h"
#include <array>
#include <string>

void magnetization_graph() {

  gStyle->SetOptStat(2210);

  TGraph* graph = new TGraph("/home/matteo/root/macros/ProgettoBazzani/sim_data_p=tanh1/magn_data/magn_data_n100_t300_d1.csv", "%lg %lg");
  graph->SetTitle("Evoluzione Temporale della Magnetizzazione per d=1; t (u.t.a.); M");
  graph->SetMarkerStyle(8);
  graph->SetMarkerSize(1);
  graph->SetMarkerColor(kBlue+1);
  graph->SetLineColor(kBlue);
  graph->SetLineWidth(1);
  graph->GetXaxis()->SetLimits(0,300);
  graph->SetMinimum(-1.);
  graph->SetMaximum(1.);
  graph->GetXaxis()->SetLabelFont(132); 
  graph->GetXaxis()->SetTitleFont(132); 
  graph->GetYaxis()->SetLabelFont(132); 
  graph->GetYaxis()->SetTitleFont(132); 

// Window for Visualization of Magnetization
  TCanvas* c = new TCanvas("c1","Evoluzione Temporale della Magnetizzazione",200,10,1500,900);
  c->SetGridx();
  c->SetGridy();
  graph->Draw("ALP");

}

void try_graph() {
  TGraph* graph = new TGraph();

  ifstream file("/home/matteo/root/macros/ProgettoBazzani/try.csv");
  while (1) {
    if (!file.good()) break;
    std::string title1, title2;
    file >> title1 >> title2;

    Double_t magn;
    Int_t time;
    Int_t nrows=0;
    while (file >> magn >> time) {
      ++nrows;
      graph->SetPoint(nrows, time, magn);
    }
  }

  TCanvas* c = new TCanvas("c1","Evoluzione Temporale della Magnetizzazione",200,10,1100,900);
  graph->Draw("AP*");
}

void poland_data_graph() {

  gStyle->SetOptStat(2210);

  TGraph* graph = new TGraph();
  graph->SetTitle("Evoluzione Temporale della Magnetizzazione relativa ai Dati; t (u.t.a.); M");
  graph->SetMarkerStyle(8);
  graph->SetMarkerSize(1);
  graph->SetMarkerColor(kBlue+1);
  graph->SetLineColor(kBlue);
  graph->SetLineWidth(1);
  graph->GetXaxis()->SetLimits(0,300);
  graph->SetMinimum(-1.);
  graph->SetMaximum(1.);
  graph->GetXaxis()->SetLabelFont(132); 
  graph->GetXaxis()->SetTitleFont(132); 
  graph->GetYaxis()->SetLabelFont(132); 
  graph->GetYaxis()->SetTitleFont(132); 
  ifstream file("/home/matteo/root/macros/ProgettoBazzani/poland_data.csv");
  while (1) {
    if (!file.good()) break;
    std::string title1, title2, title3, title4, title5;
    file >> title1 >> title2 >> title3 >> title4 >> title5;

    Int_t yes, no, dontknow, months;
    std::string date;  //forse date è da togliere
    Int_t nrows=0;
    while (file >> yes >> no >> dontknow >> months >> date) {
      ++nrows;
      Double_t magn = (yes*(1.) + no*(-1.))/(yes + no + dontknow); 
      graph->SetPoint(nrows, months, magn);
    }
  }

// Window for Visualization of Magnetization
  TCanvas* c1 = new TCanvas("c1","Evoluzione Temporale della Magnetizzazione relativa ai Dati",200,10,1100,900);
  c1->SetGridx();
  c1->SetGridy();
  graph->Draw("ALP");

}

void decision_time_graph() {

}

void initial_condition_influence_graph() {

}
