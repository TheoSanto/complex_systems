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

  TGraph* graph1 = new TGraph("/partial_magn_data/partial_magn_data_n100_d4_v1.csv", "%lg %lg");
  graph1->SetTitle("; t (u.t.a.); M");
  graph1->SetLineColor(kBlue);
  graph1->SetLineWidth(3);
  graph1->GetXaxis()->SetLimits(0,300);
  graph1->GetYaxis()->SetRangeUser(-1.,1.);
  graph1->GetXaxis()->SetTitleSize(0.07);
  graph1->GetXaxis()->SetLabelSize(0.05);
  graph1->GetYaxis()->SetTitleSize(0.07);
  graph1->GetYaxis()->SetLabelSize(0.05);
  graph1->GetYaxis()->SetTitleOffset(0.7);
  graph1->GetXaxis()->SetTitleOffset(0.7);
  graph1->GetXaxis()->SetLabelFont(132); 
  graph1->GetXaxis()->SetTitleFont(132); 
  graph1->GetYaxis()->SetLabelFont(132); 
  graph1->GetYaxis()->SetTitleFont(132);

  gStyle->SetLegendFont(132);

  TLegend* leg1 = new TLegend(.1,.7,.3,.9);
  leg1->SetFillColor(0);
  leg1->AddEntry(graph1,"Magnetizzazione per #eta = 1"); 

// Window for Visualization of Magnetization
  TCanvas* c = new TCanvas("c","Evoluzione Temporale della Magnetizzazione",100,10,1300,900);
  c->SetGridx();
  c->SetGridy();
  graph8->Draw("AL");
  leg8->Draw("SAME");
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// "POLAND IN NATO?" DATA GRAPH ///////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void poland_data_graph() {

  gStyle->SetOptStat(2210);

  TGraph* graph = new TGraph();
  graph->SetMarkerStyle(8);
  graph->SetMarkerSize(1);
  graph->SetMarkerColor(kBlue+1);
  graph->SetLineColor(kBlue);
  graph->SetLineWidth(2);
  graph->GetYaxis()->SetRangeUser(-1.,1.);

  TH1F* h = new TH1F("h","",19,0.5,19.5);
  h->SetTitle("Evoluzione Temporale della Magnetizzazione relativa ai Dati; t (f.s.); M");
  h->SetNdivisions(-10);
  h->GetYaxis()->SetRangeUser(-1.,1.);
  h->GetXaxis()->SetLabelFont(132); 
  h->GetXaxis()->SetTitleFont(132); 
  h->GetYaxis()->SetLabelFont(132); 
  h->GetYaxis()->SetTitleFont(132); 
  h->SetStats(0);

  ifstream file("/poland_data.txt");
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
  TCanvas* c = new TCanvas("c","Evoluzione Temporale della Magnetizzazione relativa ai Dati",100,10,1300,900);
  c->SetGridx();
  c->SetGridy();
  h->Draw("");
  graph->Draw("L");

}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// DECISION TIME DISTRIBUTION GRAPHS /////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void decision_time_graph() {

  TGraph* graph = new TGraph();
  graph->SetTitle("Distribuzione dei Tempi di Decisione per #eta = 8; #tau (u.t.a.); #phi (#tau)");
  graph->SetMarkerStyle(25);
  graph->SetMarkerSize(1.3);
  graph->SetMarkerColor(kBlack);
  graph->GetYaxis()->SetRangeUser(0.1,1000.);
  graph->GetYaxis()->SetRangeUser(0.001,1.);
  graph->GetXaxis()->SetLabelFont(132); 
  graph->GetXaxis()->SetTitleFont(132); 
  graph->GetYaxis()->SetLabelFont(132); 
  graph->GetYaxis()->SetTitleFont(132); 

  ifstream file("/partial_time_data/partial_time_data_n100_d4_v1.csv");
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

  TF1* power = new TF1("power","[0]*(x^[1])",0.,1.);
  graph->Fit("power","R","",1.,150.);  //(110 per delta = 4, 20 per delta = 8) per Normale;  (130 per v=2, 50 per v=4, ) per Visione Parziale
  //graph->Fit("expo","R","",1.,150.); //  (150 per v=1) per Visione Parziale
  power->SetLineColor(kRed);
  power->SetLineWidth(3);

// (0.0161701 +- 0.000904924) per d=1;
// (-0.349425 +- 0.0143637)       per d=1;

// (0.0482644 +- 0.0016885)      per d=2;
// (-0.610245 +- 0.0136683)       per d=2;

// (0.140439 +- 0.00428431)      per d=4;
// (-0.916247 +- 0.0271092)       per d=4;

// (0.360684 +- 0.0140535)      per d=8;
// (-1.26885 +- 0.0684052)       per d=8;

//    0.0212399   +/-   0.000395307 
//   -0.0193598   +/-   0.00050791                per v=1;  (expo)

//    0.0637967   +/-   0.00281282   per v=2;  (power law)  
//    -0.578246   +/-   0.0181466 

//      0.19726   +/-   0.00495002   per v=4; (power law)  
//    -0.954159   +/-   0.0242264 

//     0.285587   +/-   0.00928177   per v=8;  (power law)  
//     -1.16938   +/-   0.0449825   

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

  ifstream file1("/init_data_fixed/init_data_sim500_d4_reds10_fixed.txt");
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

  ifstream file2("/init_data_fixed/init_data_sim500_d4_reds20_fixed.txt");
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

  ifstream file3("/init_data_fixed/init_data_sim500_d4_reds30_fixed.txt");
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

  ifstream file4("/init_data_fixed/init_data_sim500_d4_reds40_fixed.txt");
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

  ifstream file5("/init_data_fixed/init_data_sim500_d4_reds50_fixed.txt");
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

  ifstream file6("/init_data_fixed/init_data_sim500_d4_reds60_fixed.txt");
  while (1) {
    if (!file6.good()) break;

    Int_t stationary, final_time;
    Int_t tot_pos = 0;
    Int_t tot_neg = 0;
    Int_t nrows=0;
    while (file6  >> stationary >> final_time) {
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

  ifstream file7("/init_data_fixed/init_data_sim500_d4_reds70_fixed.txt");
  while (1) {
    if (!file7.good()) break;

    Int_t stationary, final_time;
    Int_t tot_pos = 0;
    Int_t tot_neg = 0;
    Int_t nrows=0;
    while (file7  >> stationary >> final_time) {
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

  ifstream file8("/init_data_fixed/init_data_sim500_d4_reds80_fixed.txt");
  while (1) {
    if (!file8.good()) break;

    Int_t stationary, final_time;
    Int_t tot_pos = 0;
    Int_t tot_neg = 0;
    Int_t nrows=0;
    while (file8  >> stationary >> final_time) {
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

  ifstream file9("/init_data_fixed/init_data_sim500_d4_reds90_fixed.txt");
  while (1) {
    if (!file9.good()) break;

    Int_t stationary, final_time;
    Int_t tot_pos = 0;
    Int_t tot_neg = 0;
    Int_t nrows=0;
    while (file9  >> stationary >> final_time) {
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
     g_pos->SetPoint(i,(i+1)*0.1,probs_pos[i]);
     g_neg->SetPoint(i,(i+1)*0.1,probs_neg[i]);
  }

  TF1* tanh1 = new TF1("tanh1","[0]*(TMath::TanH([1]*(x+[2])))+[3]",0.,1.);
  tanh1->SetParLimits(0,0.4,0.5);       //0.499944 +- 0.0004   (Normale & Random);    0.5 +- 0.0016                  (Normale & Fixed);
  tanh1->SetParLimits(1,0,50);           //17.3314 +- 0.1325      (Normale & Random);    4.77182 +- 0.2595         (Normale & Fixed);
  tanh1->SetParLimits(2,-0.6,-0.4);  //-0.500552 +- 0.00078 (Normale & Random);   -0.500322 +- 0.00429    (Normale & Fixed);
  tanh1->SetParLimits(3,0.4,0.6);     //0.497912 +- 0.00067  (Normale & Random);    0.493559 +- 0.003561  (Normale & Fixed);

  TF1* tanh2 = new TF1("tanh2","[0]*(TMath::TanH([1]*(x+[2])))+[3]",0.,1.);
  tanh2->SetParLimits(0,-0.5,-0.4);   //-0.499944 +- 0.0004   (Normale & Random);   -0.5 +-  0.0016            (Normale & Fixed);
  tanh2->SetParLimits(1,0,50);           //17.3314 +- 0.1325      (Normale & Random);    4.77182 +- 0.259       (Normale & Fixed);
  tanh2->SetParLimits(2,-0.6,-0.4);  //-0.500552 +- 0.00078 (Normale & Random);   -0.500322 +- 0.0042  (Normale & Fixed);
  tanh2->SetParLimits(3,0.4,0.6);      //0.502088 +- 0.00065 (Normale & Random);    0.506441 +- 0.0035  (Normale & Fixed);

  g_pos->Fit(tanh2,"R","",0.,1.);
  g_neg->Fit(tanh1,"R","",0.,1.);

  std::cout << "R2 for g_pos = " << R2(g_pos,tanh2,9) << '\n' << '\n';  // 0.999927 for Random, 0.996754 for Fixed
  std::cout << "R2 for g_neg = " << R2(g_neg,tanh1,9) << '\n';               // 0.999927 for Random, 0.996754 for Fixed

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
  tanh1->Draw("SAME");
  tanh2->Draw("SAME");
  leg->Draw("SAME");

}
