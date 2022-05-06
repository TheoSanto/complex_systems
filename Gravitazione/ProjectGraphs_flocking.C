#include "TH1.h"
#include "TRandom.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TFile.h"
#include "TStyle.h"
#include "TTree.h"
#include <array>
#include <vector>
#include <iostream>

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// R^2 FUNCTION FOR FITTING //////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

double R2(TGraph* graph, TF1* func, int N) {
  double sum1 = 0.;
  double sum2 = 0.;
  double Ymed = 0.;
  for (int i = 0; i < N; ++i) {
    Ymed += graph->GetPointY(i)/N;
  }
  for (int i = 0; i < N; ++i) {
    sum1 += (TMath::Power(graph->GetPointY(i)-func->Eval(graph->GetPointX(i)),2));
    sum2 += (TMath::Power(graph->GetPointY(i)-Ymed,2));
  }

  double sum = sum1/sum2;
  double R2 = 1 - sum;
  return R2;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  MAGNETIZATION GRAPHS ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void magnetization_graph() {

  gStyle->SetOptStat(2210);

  TGraph* graph = new TGraph("/home/theo/Scrivania/magnetizzazione_10078steps.csv", "%lg %lg");
  
  graph->SetTitle("; t (u.t.a.); M");
  graph->SetLineColor(kBlue);
  graph->SetLineWidth(3);
  //graph->GetXaxis()->SetLimits(0,500);
  graph->GetYaxis()->SetRangeUser(-1.,1.);
  graph->GetXaxis()->SetTitleSize(0.07);
  graph->GetXaxis()->SetLabelSize(0.05);
  graph->GetYaxis()->SetTitleSize(0.07);
  graph->GetYaxis()->SetLabelSize(0.05);
  graph->GetXaxis()->SetTitleOffset(0.7);
  graph->GetYaxis()->SetTitleOffset(0.7);
  graph->GetXaxis()->SetLabelFont(132); 
  graph->GetXaxis()->SetTitleFont(132); 
  graph->GetYaxis()->SetLabelFont(132); 
  graph->GetYaxis()->SetTitleFont(132); 

  TLegend* leg1 = new TLegend(.1,.7,.3,.9);
  leg1->SetFillColor(0);
  leg1->AddEntry(graph,"Magnetizzazione per #delta = 4"); //1,2,4,8
  
// Window for Visualization of Magnetization
  TCanvas* c = new TCanvas("c1","Evoluzione Temporale della Magnetizzazione",100,10,1300,900);
 
  c->SetGridx();
  c->SetGridy(); 
  graph->Draw("AL");
  leg1->Draw("SAME");
}


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// DECISION TIME DISTRIBUTION GRAPHS /////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void decision_time_graph() {

  TGraph* graph = new TGraph();
  graph->SetTitle("Distribuzione dei Tempi di Decisione per #delta = 8; #tau (u.t.a.); #phi (#tau)"); //1,2,4,8
  graph->SetMarkerStyle(25);
  graph->SetMarkerSize(1.3);
  graph->SetMarkerColor(kBlack);
  //graph->GetYaxis()->SetRangeUser(0.1,1000.);
  graph->GetYaxis()->SetRangeUser(0,1);
  graph->GetXaxis()->SetLabelFont(132); 
  graph->GetXaxis()->SetTitleFont(132); 
  graph->GetYaxis()->SetLabelFont(132); 
  graph->GetYaxis()->SetTitleFont(132); 

  ifstream file("/home/theo/Scrivania/grav_time_data_d8_t500.csv");
  std::vector<Int_t> decision_times;
  std::vector<Double_t> frequencies;
  std::vector<Int_t> each_counts;
  Int_t one_cycle = 0;
  while (1) {
    if (!file.good()) break;
    std::string title1, title2;
    file >> title1 >> title2;

    Int_t counts, decision_time;
    Int_t tot_counts = 0;
    Int_t nrows=0;
    while (file  >> decision_time >> counts) {
       if (nrows==298) { ++one_cycle; break; }
      ++nrows;
       tot_counts += counts;
       each_counts.push_back(counts);
       decision_times.push_back(decision_time);
    }
    for (int i = 0; i<nrows; i++) {
        Double_t freq = ((double)each_counts[i])/((double)tot_counts);
        frequencies.push_back(freq);
	graph->SetPoint(i, decision_times[i], freq);
    }
    if (one_cycle==1) { break; }
  }

  TF1* power = new TF1("power","[0]*(x^[1])",0.,100.);
  //graph->Fit("power", "R", "", 1., 100.);//(28 per t10078, 27.5 per d1, 23 per d2 e d4 e d8)
  graph->Fit("expo","R","",1.,20.);  //(150 per v=1) per Visione Parziale
  power->SetLineColor(kRed);
  power->SetLineWidth(3);
  gStyle->SetLegendFont(132);

  TLegend* leg = new TLegend(.1,.7,.3,.9);
  leg->SetFillColor(0);
  leg->AddEntry(graph,"Dati sperimentali");
  leg->AddEntry(power,"Fit di power law");

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  TCanvas* c = new TCanvas("c","Distribuzione dei Tempi di Decisione",200,10,1100,900);
  c->SetLogx();
  c->SetLogy();
  graph->Draw("AP");
  leg->Draw("SAME");
  std::cout<<"Coefficiente di determinazione :"<<R2(graph, power,131)<<'\n';
  }


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// PROBABILITY OF STATIONARY STATES ///////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void initial_condition_influence_graph() {

  TGraph* g_pos = new TGraph();
  g_pos->SetMarkerStyle(8);
  g_pos->SetMarkerSize(1);
  g_pos->SetMarkerColor(kBlue+1);

  TGraph* g_neg = new TGraph();
  g_neg->SetMarkerStyle(8);
  g_neg->SetMarkerSize(1);
  g_neg->SetMarkerColor(kRed+1);
 
  std::vector<Double_t> probs_pos;
  std::vector<Double_t> probs_neg;

  ifstream file1("/home/theo/Scrivania/10_red.txt");
  while (1) {
    if (!file1.good()) break;

    Int_t stationary, final_time;
    Int_t tot_pos = 0;
    Int_t tot_neg = 0;
    Int_t nrows=0;
    while (file1  >> stationary >> final_time) {
      ++nrows;
      if (stationary==+1) {
       tot_pos += 1;
       }
       if (stationary==-1) {
       tot_neg += 1;
       }
    }
    Double_t prob_pos = ((double)tot_pos)/((double)(tot_pos + tot_neg));
    Double_t prob_neg = ((double)tot_neg)/((double)(tot_pos + tot_neg));
    probs_pos.push_back(prob_pos);
    probs_neg.push_back(prob_neg);
  }

  ifstream file2("/home/theo/Scrivania/30_red.txt");
  while (1) {
    if (!file2.good()) break;

    Int_t stationary, final_time;
    Int_t tot_pos = 0;
    Int_t tot_neg = 0;
    Int_t nrows=0;
    while (file2  >> stationary >> final_time) {
      ++nrows;
       if (stationary==+1) {
       tot_pos += 1;
       }
       if (stationary==-1) {
       tot_neg += 1;
       }
    }
    Double_t prob_pos = ((double)tot_pos)/((double)(tot_pos + tot_neg));
    Double_t prob_neg = ((double)tot_neg)/((double)(tot_pos + tot_neg));
    probs_pos.push_back(prob_pos);
    probs_neg.push_back(prob_neg);
  }

  ifstream file3("/home/theo/Scrivania/50_red.txt");
  while (1) {
    if (!file3.good()) break;

    Int_t stationary, final_time;
    Int_t tot_pos = 0;
    Int_t tot_neg = 0;
    Int_t nrows=0;
    while (file3  >> stationary >> final_time) {
      ++nrows;
       if (stationary==+1) {
       tot_pos += 1;
       }
       if (stationary==-1) {
       tot_neg += 1;
       }
    }
    Double_t prob_pos = ((double)tot_pos)/((double)(tot_pos + tot_neg));
    Double_t prob_neg = ((double)tot_neg)/((double)(tot_pos + tot_neg));
    probs_pos.push_back(prob_pos);
    probs_neg.push_back(prob_neg);
  }

  ifstream file4("/home/theo/Scrivania/70_red.txt");
  while (1) {
    if (!file4.good()) break;

    Int_t stationary, final_time;
    Int_t tot_pos = 0;
    Int_t tot_neg = 0;
    Int_t nrows=0;
    while (file4  >> stationary >> final_time) {
      ++nrows;
       if (stationary==+1) {
       tot_pos += 1;
       }
       if (stationary==-1) {
       tot_neg += 1;
       }
    }
    Double_t prob_pos = ((double)tot_pos)/((double)(tot_pos + tot_neg));
    Double_t prob_neg = ((double)tot_neg)/((double)(tot_pos + tot_neg));
    probs_pos.push_back(prob_pos);
    probs_neg.push_back(prob_neg);
  }

  ifstream file5("/home/theo/Scrivania/90_red.txt");
  while (1) {
    if (!file5.good()) break;

    Int_t stationary, final_time;
    Int_t tot_pos = 0;
    Int_t tot_neg = 0;
    Int_t nrows=0;
    while (file5  >> stationary >> final_time) {
      ++nrows;
       if (stationary==+1) {
       tot_pos += 1;
       }
       if (stationary==-1) {
       tot_neg += 1;
       }
    }
    Double_t prob_pos = ((double)tot_pos)/((double)(tot_pos + tot_neg));
    Double_t prob_neg = ((double)tot_neg)/((double)(tot_pos + tot_neg));
    probs_pos.push_back(prob_pos);
    probs_neg.push_back(prob_neg);
  }
 
  for (int i = 0; i<probs_pos.size(); i++) {
     g_pos->SetPoint(i,(2*i+1)*0.1,probs_pos[i]);
     g_neg->SetPoint(i,(2*i+1)*0.1,probs_neg[i]);
  }

  TF1* tanh1 = new TF1("tanh1","[0]*(TMath::TanH([1]*(x+[2])))+[3]",0.,1.);
  tanh1->SetParLimits(0, 0.4,0.5);
  tanh1->SetParLimits(1, 4, 5);   
  tanh1->SetParLimits(2, -0.5, -0.3);
  tanh1->SetParLimits(3, 0.4,0.6);    

  TF1* tanh2 = new TF1("tanh2","[0]*(TMath::TanH([1]*(x+[2])))+[3]",0.,1.);
  tanh2->SetParLimits(0,-0.5,-0.4);  
  tanh2->SetParLimits(1,4, 5); 
  tanh2->SetParLimits(2,-0.5,-0.3); 
  tanh2->SetParLimits(3,0.4,0.6);  

  g_pos->Fit(tanh2,"R","",0.,1.);
  g_neg->Fit(tanh1,"R","",0.,1.);

  tanh2->SetLineColor(kBlue);
  tanh2->SetLineWidth(3);
  tanh2->SetLineStyle(9);
  tanh1->SetLineColor(kRed);
  tanh1->SetLineWidth(3);
  tanh1->SetLineStyle(9);

 TMultiGraph *graphs = new TMultiGraph();
  graphs->Add(g_pos);  
  graphs->Add(g_neg);  
  graphs->SetTitle("Probabilita' di Osservazione delle Distribuzioni Stazionarie; c^{in}_{-}; P (c^{in}_{-})");
  graphs->GetXaxis()->SetLimits(0,1);
  graphs->GetYaxis()->SetRangeUser(-0.1,1.1);
  graphs->GetXaxis()->SetLabelFont(132); 
  graphs->GetXaxis()->SetTitleFont(132); 
  graphs->GetYaxis()->SetLabelFont(132); 
  graphs->GetYaxis()->SetTitleFont(132); 

  gStyle->SetLegendFont(132);

  TLegend *leg = new TLegend(.1,.7,.3,.9);
  leg->SetFillColor(0);
  leg->AddEntry(g_pos,"\"Tutti +1\"");
  leg->AddEntry(tanh2,"Fit su \"Tutti +1\"");
  leg->AddEntry(g_neg,"\"Tutti -1\"");
  leg->AddEntry(tanh1,"Fit su \"Tutti -1\"");

  TCanvas* c = new TCanvas("c","Probabilita' di Osservazione delle Condizioni Stazionarie",200,10,1100,900);
  c->SetGridx();
  c->SetGridy();
  graphs->Draw("AP");
  leg->Draw("SAME");
  
  std::cout<<"Coefficienti R2 :"<<R2(g_neg, tanh1, 5)<<'\n';
  std::cout<<"Coefficienti R2 :"<<R2(g_pos , tanh2, 5)<<'\n';
}
