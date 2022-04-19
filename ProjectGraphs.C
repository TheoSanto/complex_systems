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

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// R^2 FUNCTION FOR FITTING //////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

double R2(TGraph* graph, TF1* func, int N) {
  double sum1 = 0.;
  double sum2 = 0.;
  double Ymed = 0.;
  for (int i = 1; i <= N; ++i) {
    Ymed += graph->GetPointY(i)/N;
  }
  for (int i = 1; i <= N; ++i) {
    if (graph->GetPointX(i) <= 40000) {
    sum1 += (TMath::Power(graph->GetPointY(i)-func->Eval(graph->GetPointX(i)),2));
    sum2 += (TMath::Power(graph->GetPointY(i)-Ymed,2));
    } else {}
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

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// DECISION TIME DISTRIBUTION GRAPHS /////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

  ifstream file1("/home/matteo/root/macros/ProgettoBazzani/init_data_random/init_data_sim500_d4_reds10_random.txt");
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

  ifstream file2("/home/matteo/root/macros/ProgettoBazzani/init_data_random/init_data_sim500_d4_reds20_random.txt");
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

  ifstream file3("/home/matteo/root/macros/ProgettoBazzani/init_data_random/init_data_sim500_d4_reds30_random.txt");
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

  ifstream file4("/home/matteo/root/macros/ProgettoBazzani/init_data_random/init_data_sim500_d4_reds40_random.txt");
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

  ifstream file5("/home/matteo/root/macros/ProgettoBazzani/init_data_random/init_data_sim500_d4_reds50_random.txt");
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

  ifstream file6("/home/matteo/root/macros/ProgettoBazzani/init_data_random/init_data_sim500_d4_reds60_random.txt");
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

  ifstream file7("/home/matteo/root/macros/ProgettoBazzani/init_data_random/init_data_sim500_d4_reds70_random.txt");
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

  ifstream file8("/home/matteo/root/macros/ProgettoBazzani/init_data_random/init_data_sim500_d4_reds80_random.txt");
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

  ifstream file9("/home/matteo/root/macros/ProgettoBazzani/init_data_random/init_data_sim500_d4_reds90_random.txt");
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
}
