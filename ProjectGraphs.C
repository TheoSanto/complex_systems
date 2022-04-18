#include "TH1.h"
#include "TRandom.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TStyle.h"
#include "TTree.h"
#include <array>
#include <vector>

void magnetization_graph() {

  gStyle->SetOptStat(2210);

  TGraph* graph = new TGraph("/home/matteo/root/macros/ProgettoBazzani/sim_data_p=tanh1/magn_data/magn_data_n100_t300_d1.csv", "%lg %lg");
  graph->SetTitle("Evoluzione Temporale della Magnetizzazione per #delta =1; t (u.t.a.); M");
  graph->SetMarkerStyle(8);
  graph->SetMarkerSize(1);
  graph->SetMarkerColor(kBlue+1);
  graph->SetLineColor(kBlue);
  graph->SetLineWidth(2);
  graph->GetXaxis()->SetLimits(0,300);
  graph->SetMinimum(-1.);
  graph->SetMaximum(1.);
  graph->GetXaxis()->SetLabelFont(132); 
  graph->GetXaxis()->SetTitleFont(132); 
  graph->GetYaxis()->SetLabelFont(132); 
  graph->GetYaxis()->SetTitleFont(132); 

// Window for Visualization of Magnetization
  TCanvas* c = new TCanvas("c1","Evoluzione Temporale della Magnetizzazione",100,10,1300,900);
  c->SetGridx();
  c->SetGridy();
  graph->Draw("AL");

}

void poland_data_graph() {

  gStyle->SetOptStat(2210);

  TGraph* graph = new TGraph();
  graph->SetMarkerStyle(8);
  graph->SetMarkerSize(1);
  graph->SetMarkerColor(kBlue+1);
  graph->SetLineColor(kBlue);
  graph->SetLineWidth(2);
  graph->SetMaximum(1.);

  TH1F* h = new TH1F("h","",19,0.5,19.5);
  h->SetTitle("Evoluzione Temporale della Magnetizzazione relativa ai Dati; t (u.t.a.); M");
  h->SetNdivisions(-10);
  h->GetXaxis()->SetLabelFont(132); 
  h->GetXaxis()->SetTitleFont(132); 
  h->GetYaxis()->SetLabelFont(132); 
  h->GetYaxis()->SetTitleFont(132); 
  h->SetStats(0);

  ifstream file("/home/matteo/root/macros/ProgettoBazzani/poland_data.txt");
  while (1) {
    if (!file.good()) break;
    std::string title1, title2, title3, title4, title5, title6;
    file >> title1 >> title2 >> title3 >> title4 >> title5 >> title6;

    Int_t yes, no, dontknow, false_months, real_months;
    char* date;
    Int_t nrows=0;
    while (file >> yes >> no >> dontknow >> false_months >> real_months >> date) {
      ++nrows;
      Double_t magn = (yes*(1.) + no*(-1.))/(yes + no + dontknow); 
      graph->SetPoint(nrows, false_months, magn);
      h->GetXaxis()->SetBinLabel(nrows,date);
      if (nrows==10) {
          h->GetXaxis()->SetBinLabel(10,"--");
      }
    }
  }


// Window for Visualization of Magnetization
  TCanvas* c1 = new TCanvas("c1","Evoluzione Temporale della Magnetizzazione relativa ai Dati",100,10,1300,900);
  c1->SetGridx();
  c1->SetGridy();
  h->Draw("");
  graph->Draw("L");

}

void decision_time_graph() {
  TGraph* graph = new TGraph();
  graph->SetTitle("Distribuzione dei Tempi di Decisione per #delta =1; #tau (u.t.a.); #phi (#tau)");
  graph->SetMarkerStyle(8);
  graph->SetMarkerSize(1);
  graph->SetMarkerColor(kBlue+1);
/*  graph->GetXaxis()->SetLimits(0,300);
  graph->SetMinimum(-1.);
  graph->SetMaximum(1.); */
  graph->GetXaxis()->SetLabelFont(132); 
  graph->GetXaxis()->SetTitleFont(132); 
  graph->GetYaxis()->SetLabelFont(132); 
  graph->GetYaxis()->SetTitleFont(132); 

  ifstream file("/home/matteo/root/macros/ProgettoBazzani/sim_data_p=tanh1/time_data/time_data_n100_t300_d1.csv");
  std::vector<Int_t> decision_times;
  std::vector<Double_t> frequencies;
  std::vector<Int_t> each_counts;
  while (1) {
    if (!file.good()) break;
    std::string title1, title2;
    file >> title1 >> title2;

    Int_t counts, decision_time;
    Int_t tot_counts = 0;
    Int_t nrows=0;
    while (file  >> decision_time >> counts) {
      ++nrows;
       tot_counts += counts;
       each_counts.push_back(counts);
       decision_times.push_back(decision_time);
      //graph->SetPoint(nrows, time, magn);
    }
    for (int i = 0; i<nrows; i++) {
        Double_t freq = ((double)each_counts[i])/((double)tot_counts);
        frequencies.push_back(freq);
	graph->SetPoint(i, decision_times[i], freq);
    }
  }

  graph->Fit("expo");

  TCanvas* c = new TCanvas("c1","Distribuzione dei Tempi di Decisione",200,10,1100,900);
/*c->SetGridx();
  c->SetGridy(); */
  c->SetLogx();
  c->SetLogy();
  graph->Draw("AP");
}

void initial_condition_influence_graph() {

}
