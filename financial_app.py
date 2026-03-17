import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="KFintech Enterprise Suite v7.2", layout="wide", initial_sidebar_state="expanded")

# === ENTERPRISE BANKING CSS ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.main {font-family: 'Inter', sans-serif;}
.header-main {font-size: 2.8rem; font-weight: 700; color: #1e293b; text-align: center; line-height: 1.2;}
.subheader-main {font-size: 1.2rem; color: #64748b; text-align: center; font-weight: 500;}
.metric-card {background: white; padding: 1.8rem; border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.08);}
.status-approved {background: linear-gradient(135deg, #059669, #047857); color: white;}
.status-review {background: linear-gradient(135deg, #d97706, #b45309); color: white;}
.status-rejected {background: linear-gradient(135deg, #dc2626, #b91c1c); color: white;}
.issues-panel {background: #fef7ed; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #f97316;}
.product-card {background: linear-gradient(135deg, #f8fafc, #f1f5f9); padding: 2rem; border-radius: 16px;}
.error-free {border: 2px solid #10b981; background: #f0fdf4;}
</style>
""", unsafe_allow_html=True)

# === CLEAN HEADER ===
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8fafc, #e2e8f0); border-radius: 20px;'>
    <h1 class="header-main">🏦 KFintech Enterprise Financial Suite v7.2</h1>
    <p class="subheader-main">Madhu Kumar | AI Business Analyst | Production Banking Platform</p>
</div>
""", unsafe_allow_html=True)

# === PRODUCT NAVIGATION ===
st.sidebar.title("🎯 Product Suite")
product = st.sidebar.selectbox("Select Calculator", [
    "💳 Loans (7 Types)", "💎 AIF HNI Check", "📈 MF SIP Calculator", 
    "🛡️ Term Insurance", "📊 EMI Amortization"
])

# === 1. LOANS - FIXED REJECTION BOX READABILITY ===
if product == "💳 Loans (7 Types)":
    st.markdown('<div class="product-card"><h2>💳 Complete Loan Eligibility Engine (RBI Compliant)</h2></div>', unsafe_allow_html=True)
    
    loan_products = {
        "🏠 Home Loan": {"rate": 8.50, "tenure_max": 360, "min_income": 50000, "dtl_max": 0.50},
        "💳 Personal Loan": {"rate": 11.50, "tenure_max": 60, "min_income": 30000, "dtl_max": 0.50},
        "🚗 Car Loan": {"rate": 9.00, "tenure_max": 84, "min_income": 40000, "dtl_max": 0.50},
        "📚 Education": {"rate": 10.50, "tenure_max": 180, "min_income": 25000, "dtl_max": 0.60},
        "💰 Gold Loan": {"rate": 9.50, "tenure_max": 36, "min_income": 20000, "dtl_max": 0.75},
        "🏢 Business": {"rate": 12.00, "tenure_max": 120, "min_income": 75000, "dtl_max": 0.60},
        "💳 Credit Card": {"rate": 36.00, "tenure_max": 12, "min_income": 25000, "dtl_max": 0.40}
    }
    
    col1, col2, col3 = st.columns(3)
    with col1:
        loan_type = st.selectbox("Loan Product", list(loan_products.keys()))
        principal = st.number_input("💰 Loan Amount (₹)", min_value=100000, max_value=500000000, value=2500000)
    with col2:
        max_tenure = loan_products[loan_type]["tenure_max"]
        tenure_months = st.slider("📅 Tenure (Months)", 1, max_tenure, 60)
        rate_annual = st.number_input("📊 Interest Rate (%)", 6.0, 40.0, loan_products[loan_type]["rate"])
    with col3:
        monthly_income = st.number_input("💼 Monthly Income (₹)", 15000, 5000000, 75000)
    
    col1, col2 = st.columns(2)
    with col1:
        existing_emi = st.number_input("💸 Existing Monthly EMI (₹)", 0, 200000, 0)
        cibil_score = st.slider("⭐ CIBIL Score", 300, 900, 750)
    with col2:
        dependents = st.slider("👨‍👩‍👧‍👦 No. of Dependents", 0, 10, 2)
        age = st.slider("👤 Age", 21, 65, 35)
    
    if st.button("🚀 **ANALYZE COMPLETE ELIGIBILITY**", type="primary", use_container_width=True):
        rate_monthly = rate_annual / 12 / 100
        if rate_monthly == 0:
            emi = principal / tenure_months
        else:
            power_term = (1 + rate_monthly) ** tenure_months
            emi = principal * rate_monthly * power_term / (power_term - 1)
        
        total_emi = emi + existing_emi
        disposable_income = monthly_income * 0.65
        living_expense_per_dep = 5000 * dependents
        net_disposable = max(0, disposable_income - living_expense_per_dep)
        dti_ratio = total_emi / monthly_income
        policy_dti_limit = loan_products[loan_type]["dtl_max"]
        dti_headroom = (policy_dti_limit - dti_ratio) * 100
        emi_to_surplus_ratio = 0 if net_disposable == 0 else total_emi / net_disposable
        cibil_band = "Excellent" if cibil_score >= 780 else "Good" if cibil_score >= 730 else "Fair" if cibil_score >= 680 else "Weak"

        # Credit underwriting scorecard (100-point model)
        score_cibil = max(0, min(35, (cibil_score - 300) / 600 * 35))
        score_dti = max(0, min(30, (1 - (dti_ratio / max(policy_dti_limit, 0.01))) * 30))
        income_surplus_ratio = 0 if total_emi == 0 else net_disposable / total_emi
        score_surplus = max(0, min(20, income_surplus_ratio * 10))
        age_score_map = {
            "high": 15,
            "moderate": 10,
            "watch": 6,
            "elevated": 2
        }
        age_band = "high" if age <= 45 else "moderate" if age <= 55 else "watch" if age <= 60 else "elevated"
        score_age = age_score_map[age_band]
        underwriting_score = score_cibil + score_dti + score_surplus + score_age

        if underwriting_score >= 80:
            underwriting_grade = "A"
            underwriting_risk = "Low Risk"
        elif underwriting_score >= 65:
            underwriting_grade = "B"
            underwriting_risk = "Moderate Risk"
        elif underwriting_score >= 50:
            underwriting_grade = "C"
            underwriting_risk = "High Risk"
        else:
            underwriting_grade = "D"
            underwriting_risk = "Very High Risk"
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📉 New Loan EMI", f"₹{emi:,.0f}")
        col2.metric("💰 Total EMI", f"₹{total_emi:,.0f}")
        col3.metric("📊 DTI Ratio", f"{dti_ratio*100:.1f}%")
        col4.metric("💸 Net Disposable", f"₹{net_disposable:,.0f}")

        uw1, uw2, uw3 = st.columns(3)
        uw1.metric("🧮 Underwriting Score", f"{underwriting_score:.1f}/100")
        uw2.metric("🏷️ Underwriting Grade", underwriting_grade)
        uw3.metric("⚠️ Underwriting Risk", underwriting_risk)
        
        issues = []
        if dti_ratio > loan_products[loan_type]["dtl_max"]: 
            issues.append(f"❌ DTI {dti_ratio*100:.1f}% > {loan_products[loan_type]['dtl_max']*100:.0f}% limit")
        if total_emi > net_disposable: 
            issues.append(f"❌ Total EMI ₹{total_emi:,.0f} > Net Disposable ₹{net_disposable:,.0f}")
        if cibil_score < 650: 
            issues.append("❌ CIBIL Score < 650")
        if monthly_income < loan_products[loan_type]["min_income"]: 
            issues.append("❌ Income below product minimum")
        if age > 60 and loan_type != "💰 Gold Loan": 
            issues.append("❌ Age > 60 for long tenure products")
        
        status_class = "status-approved" if len(issues)==0 else "status-review" if len(issues)<=1 else "status-rejected"
        status_text = "✅ APPROVED" if len(issues)==0 else "⚠️ REVIEW" if len(issues)<=1 else "❌ REJECTED"
        
        st.markdown(f'''
        <div class="metric-card {status_class}" style="padding: 2.5rem; text-align: center; margin: 2rem 0; font-size: 1.1rem;">
            <h2 style="margin: 0 0 1rem 0; font-size: 2.2rem;">{status_text}</h2>
            <p style="font-size: 1.1rem; opacity: 0.9;">RBI Compliant Analysis Complete</p>
        </div>
        ''', unsafe_allow_html=True)
        
        if issues:
            with st.container():
                st.markdown("### 📋 **Issues to Address:**")
                for issue in issues:
                    st.error(issue)

        # ── helpers ──────────────────────────────────────────────────────────
        def badge(passed):
            if passed:
                return "<span style='background:#059669;color:white;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:600;letter-spacing:0.04em;'>✔ PASS</span>"
            return "<span style='background:#dc2626;color:white;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:600;letter-spacing:0.04em;'>✘ FAIL</span>"

        def score_bar(score, max_score):
            pct = min(100, score / max_score * 100)
            color = "#059669" if pct >= 70 else "#d97706" if pct >= 45 else "#dc2626"
            return f"""
            <div style='background:#e2e8f0;border-radius:6px;height:10px;width:100%;margin-top:4px;'>
                <div style='background:{color};width:{pct:.0f}%;height:10px;border-radius:6px;'></div>
            </div>"""

        grade_color = {"A": "#059669", "B": "#0284c7", "C": "#d97706", "D": "#dc2626"}
        rec_color   = "#0f4c2a" if len(issues) == 0 else "#7c3a00" if len(issues) == 1 else "#7f1d1d"
        rec_bg      = "#f0fdf4" if len(issues) == 0 else "#fffbeb" if len(issues) == 1 else "#fef2f2"
        rec_border  = "#059669" if len(issues) == 0 else "#d97706" if len(issues) == 1 else "#dc2626"
        rec_icon    = "✅" if len(issues) == 0 else "⚠️" if len(issues) == 1 else "🚫"
        rec_decision = "RECOMMEND FOR SANCTION" if len(issues) == 0 else "CONDITIONAL APPROVAL — DEVIATION NOTED" if len(issues) == 1 else "RECOMMEND DECLINE"
        if len(issues) == 0:
            rec_text = (
                "The applicant satisfies all policy filters across income adequacy, credit bureau quality, "
                "debt-service capacity, and age suitability. Sanction may be progressed subject to standard "
                "KYC documentation, income proof verification (last 3 months' salary slips / 2 years' ITR), "
                "and a bureau refresh at the time of disbursal."
            )
        elif len(issues) == 1:
            rec_text = (
                "The application carries one policy deviation. A conditional sanction may be considered "
                "subject to a compensating mitigation — options include reducing the requested ticket size, "
                "adding a financially eligible co-applicant, or restructuring the tenure within product limits. "
                "Credit committee review recommended before issuance of sanction letter."
            )
        else:
            rec_text = (
                "Multiple policy parameters are breached. The application is not financeable in its current "
                "structure. A fresh proposal may be considered only upon material improvement in bureau standing, "
                "reduction of existing obligations, or a significant increase in verified income. "
                "Customer may be advised to reapply after 6 months with revised financials."
            )

        policy_checks = [
            ("Minimum Income Requirement",  f"Actual ₹{monthly_income:,.0f} vs Floor ₹{loan_products[loan_type]['min_income']:,.0f}",  monthly_income >= loan_products[loan_type]['min_income']),
            ("Credit Bureau Score (≥ 650)", f"CIBIL {cibil_score} ({cibil_band})",                                                    cibil_score >= 650),
            ("Debt-to-Income Ratio",        f"{dti_ratio*100:.2f}% vs Policy Cap {policy_dti_limit*100:.0f}%",                        dti_ratio <= policy_dti_limit),
            ("Cash-Surplus Coverage",       f"Surplus ₹{net_disposable:,.0f} vs Total EMI ₹{total_emi:,.0f}",                        total_emi <= net_disposable),
            ("Age Suitability",             f"Age {age} yrs — {'Within limit' if not (age > 60 and loan_type != '💰 Gold Loan') else 'Exceeds 60 for this product'}", not (age > 60 and loan_type != "💰 Gold Loan")),
        ]
        policy_rows = "".join(
            f"""<tr style='border-bottom:1px solid #e2e8f0;'>
                  <td style='padding:10px 14px;font-weight:500;color:#1e293b;'>{name}</td>
                  <td style='padding:10px 14px;color:#475569;font-size:0.9rem;'>{detail}</td>
                  <td style='padding:10px 14px;text-align:center;'>{badge(ok)}</td>
               </tr>"""
            for name, detail, ok in policy_checks
        )

        scorecard_rows = "".join(
            f"""<tr style='border-bottom:1px solid #e2e8f0;'>
                  <td style='padding:10px 14px;font-weight:500;color:#1e293b;'>{factor}</td>
                  <td style='padding:10px 14px;color:#475569;font-size:0.9rem;text-align:center;'>{weight}</td>
                  <td style='padding:10px 14px;text-align:center;font-weight:700;color:#1e40af;'>{score:.1f}</td>
                  <td style='padding:10px 14px;width:200px;'>{score_bar(score, weight)}</td>
               </tr>"""
            for factor, weight, score in [
                ("CIBIL / Bureau Quality",      35, score_cibil),
                ("Debt-to-Income Capacity",     30, score_dti),
                ("Cash Surplus Coverage",       20, score_surplus),
                ("Age & Tenure Stability",      15, score_age),
            ]
        )

        st.markdown(f"""
        <div style='border:1px solid #e2e8f0;border-radius:16px;overflow:hidden;margin-top:2rem;font-family:Inter,sans-serif;'>

          <!-- Report Header -->
          <div style='background:linear-gradient(135deg,#1e293b,#1e40af);padding:1.6rem 2rem;display:flex;justify-content:space-between;align-items:center;'>
            <div>
              <span style='color:#93c5fd;font-size:0.78rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;'>KFintech Enterprise Credit Division</span>
              <h2 style='color:white;margin:4px 0 0 0;font-size:1.5rem;font-weight:700;'>Credit Underwriting Report</h2>
            </div>
            <div style='text-align:right;'>
              <span style='background:rgba(255,255,255,0.15);color:white;padding:6px 16px;border-radius:20px;font-size:0.82rem;font-weight:600;'>
                RBI Compliant · {pd.Timestamp.now().strftime("%d %b %Y")}
              </span>
            </div>
          </div>

          <!-- Section 1: Applicant & Financial Profile -->
          <div style='display:grid;grid-template-columns:1fr 1fr;gap:0;border-bottom:1px solid #e2e8f0;'>
            <div style='padding:1.4rem 2rem;border-right:1px solid #e2e8f0;'>
              <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 12px 0;'>Applicant Profile</p>
              <table style='width:100%;border-collapse:collapse;font-size:0.9rem;'>
                <tr><td style='color:#64748b;padding:4px 0;'>Product</td><td style='color:#1e293b;font-weight:600;text-align:right;'>{loan_type}</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Loan Amount</td><td style='color:#1e293b;font-weight:600;text-align:right;'>₹{principal:,.0f}</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Tenure</td><td style='color:#1e293b;font-weight:600;text-align:right;'>{tenure_months} months</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Interest Rate</td><td style='color:#1e293b;font-weight:600;text-align:right;'>{rate_annual:.2f}% p.a.</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Age / Dependents</td><td style='color:#1e293b;font-weight:600;text-align:right;'>{age} yrs / {dependents}</td></tr>
              </table>
            </div>
            <div style='padding:1.4rem 2rem;'>
              <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 12px 0;'>Income & Obligation Snapshot</p>
              <table style='width:100%;border-collapse:collapse;font-size:0.9rem;'>
                <tr><td style='color:#64748b;padding:4px 0;'>Monthly Income</td><td style='color:#1e293b;font-weight:600;text-align:right;'>₹{monthly_income:,.0f}</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Pre-existing Obligations</td><td style='color:#1e293b;font-weight:600;text-align:right;'>₹{existing_emi:,.0f}</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Proposed EMI</td><td style='color:#1e293b;font-weight:600;text-align:right;'>₹{emi:,.0f}</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Total EMI Post-Sanction</td><td style='color:#dc2626;font-weight:700;text-align:right;'>₹{total_emi:,.0f}</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Net Disposable (65% rule)</td><td style='color:#059669;font-weight:700;text-align:right;'>₹{net_disposable:,.0f}</td></tr>
              </table>
            </div>
          </div>

          <!-- Section 2: Bureau & Repayment Assessment -->
          <div style='padding:1.4rem 2rem;border-bottom:1px solid #e2e8f0;'>
            <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 14px 0;'>Credit Bureau & Repayment Capacity Assessment</p>
            <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;'>
              <div style='background:#f8fafc;border-radius:10px;padding:12px 16px;border:1px solid #e2e8f0;'>
                <p style='color:#64748b;font-size:0.75rem;margin:0 0 4px 0;'>CIBIL Score</p>
                <p style='color:#1e293b;font-size:1.4rem;font-weight:700;margin:0;'>{cibil_score}</p>
                <p style='color:#3b82f6;font-size:0.8rem;margin:4px 0 0 0;font-weight:600;'>{cibil_band}</p>
              </div>
              <div style='background:#f8fafc;border-radius:10px;padding:12px 16px;border:1px solid #e2e8f0;'>
                <p style='color:#64748b;font-size:0.75rem;margin:0 0 4px 0;'>DTI Ratio</p>
                <p style='color:{"#dc2626" if dti_ratio > policy_dti_limit else "#059669"};font-size:1.4rem;font-weight:700;margin:0;'>{dti_ratio*100:.1f}%</p>
                <p style='color:#64748b;font-size:0.8rem;margin:4px 0 0 0;'>Cap: {policy_dti_limit*100:.0f}% | Headroom: {dti_headroom:+.1f}pp</p>
              </div>
              <div style='background:#f8fafc;border-radius:10px;padding:12px 16px;border:1px solid #e2e8f0;'>
                <p style='color:#64748b;font-size:0.75rem;margin:0 0 4px 0;'>EMI/Surplus Ratio</p>
                <p style='color:{"#dc2626" if emi_to_surplus_ratio > 1 else "#059669"};font-size:1.4rem;font-weight:700;margin:0;'>{emi_to_surplus_ratio:.2f}x</p>
                <p style='color:#64748b;font-size:0.8rem;margin:4px 0 0 0;'>{"Above threshold" if emi_to_surplus_ratio > 1 else "Within threshold"}</p>
              </div>
              <div style='background:{grade_color.get(underwriting_grade,"#1e293b")};border-radius:10px;padding:12px 16px;'>
                <p style='color:rgba(255,255,255,0.8);font-size:0.75rem;margin:0 0 4px 0;'>Underwriting Grade</p>
                <p style='color:white;font-size:1.8rem;font-weight:800;margin:0;'>{underwriting_grade}</p>
                <p style='color:rgba(255,255,255,0.85);font-size:0.8rem;margin:4px 0 0 0;'>{underwriting_risk} · {underwriting_score:.0f}/100</p>
              </div>
            </div>
          </div>

          <!-- Section 3: Policy Compliance -->
          <div style='padding:1.4rem 2rem;border-bottom:1px solid #e2e8f0;'>
            <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 12px 0;'>Policy Compliance Matrix</p>
            <table style='width:100%;border-collapse:collapse;font-size:0.88rem;'>
              <thead>
                <tr style='background:#f1f5f9;'>
                  <th style='padding:10px 14px;text-align:left;color:#475569;font-weight:600;border-radius:8px 0 0 8px;'>Control</th>
                  <th style='padding:10px 14px;text-align:left;color:#475569;font-weight:600;'>Detail</th>
                  <th style='padding:10px 14px;text-align:center;color:#475569;font-weight:600;border-radius:0 8px 8px 0;'>Status</th>
                </tr>
              </thead>
              <tbody>{policy_rows}</tbody>
            </table>
          </div>

          <!-- Section 4: Scoring Breakdown -->
          <div style='padding:1.4rem 2rem;border-bottom:1px solid #e2e8f0;'>
            <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 12px 0;'>Credit Scorecard Breakdown</p>
            <table style='width:100%;border-collapse:collapse;font-size:0.88rem;'>
              <thead>
                <tr style='background:#f1f5f9;'>
                  <th style='padding:10px 14px;text-align:left;color:#475569;font-weight:600;'>Factor</th>
                  <th style='padding:10px 14px;text-align:center;color:#475569;font-weight:600;'>Max Weight</th>
                  <th style='padding:10px 14px;text-align:center;color:#475569;font-weight:600;'>Score</th>
                  <th style='padding:10px 14px;text-align:left;color:#475569;font-weight:600;'>Distribution</th>
                </tr>
              </thead>
              <tbody>{scorecard_rows}</tbody>
              <tfoot>
                <tr style='background:#eff6ff;'>
                  <td style='padding:10px 14px;font-weight:700;color:#1e40af;'>Total</td>
                  <td style='padding:10px 14px;text-align:center;font-weight:700;color:#1e40af;'>100</td>
                  <td style='padding:10px 14px;text-align:center;font-weight:800;color:#1e40af;font-size:1.05rem;'>{underwriting_score:.1f}</td>
                  <td style='padding:10px 14px;'>{score_bar(underwriting_score, 100)}</td>
                </tr>
              </tfoot>
            </table>
          </div>

          <!-- Section 5: Underwriter Recommendation -->
          <div style='padding:1.6rem 2rem;background:{rec_bg};border-left:5px solid {rec_border};margin:0;'>
            <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 6px 0;'>Underwriter Recommendation</p>
            <p style='color:{rec_color};font-size:1.1rem;font-weight:700;margin:0 0 8px 0;'>{rec_icon} {rec_decision}</p>
            <p style='color:{rec_color};font-size:0.92rem;margin:0;line-height:1.65;'>{rec_text}</p>
          </div>

        </div>
        """, unsafe_allow_html=True)

# === 2. AIF HNI - FIXED SOURCE VALIDATION DROPDOWN ===
elif product == "💎 AIF HNI Check":
    st.markdown('<div class="product-card"><h2>💎 AIF Investor Eligibility — HNI Accreditation · KYC/AML · Risk Profile (SEBI Compliant)</h2></div>', unsafe_allow_html=True)

    # ── Section 1: Financial Profile ────────────────────────────────────────
    st.markdown("#### 💰 Section 1 — Financial Profile")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        investment_cr       = st.number_input("💰 Investment Amount (₹ Cr)", 0.1, 100.0, 1.0)
    with c2:
        annual_income_lakhs = st.number_input("💼 Annual Income (₹ Lakhs)", 1.0, 1000.0, 50.0)
    with c3:
        net_worth_cr        = st.number_input("💎 Net Worth (₹ Cr)", 0.1, 500.0, 5.0)
    with c4:
        liquid_assets_cr    = st.number_input("💧 Liquid Assets (₹ Cr)", 0.1, 100.0, 2.0)

    allowed_sources = ["Salary/Business Income","Investments/Dividends","Rental Income",
                       "Inheritance","Business Sale","Retirement Corpus","Stock Options"]
    blocked_sources = ["Gambling/Lottery","Cryptocurrency Trading","Smuggling/Illegal",
                       "Unexplained Cash","Hawala Transactions","Black Money"]
    c1, c2 = st.columns(2)
    with c1:
        income_source    = st.selectbox("✅ Primary Source of Wealth", allowed_sources)
    with c2:
        selected_blocked = st.multiselect("❌ Blocked Sources (auto-reject on any selection)", blocked_sources, default=[])

    st.divider()

    # ── Section 2: KYC / AML ────────────────────────────────────────────────
    st.markdown("#### 🔍 Section 2 — KYC / AML & Sanctions Screening")
    c1, c2, c3 = st.columns(3)
    with c1:
        pan_verified             = st.selectbox("🪪 PAN Verification",        ["Verified with ITD", "Pending", "Mismatch / Not Available"])
        aadhaar_verified         = st.selectbox("🪪 Aadhaar / OVD",           ["Verified (UIDAI e-KYC)", "Paper KYC Pending", "Not Submitted"])
        cvl_kyc                  = st.selectbox("📋 CVL / KRA KYC Status",    ["KYC Compliant", "In-Progress", "Not Done"])
    with c2:
        demat_account            = st.selectbox("📂 Demat Account",           ["Active & Linked", "Active, Not Linked", "Not Available"])
        investment_account_type  = st.selectbox("🏦 Bank Account Type",       ["Resident Individual", "NRI – NRE/NRO", "Foreign National"])
        ubo_declared             = st.selectbox("👤 UBO Declaration",         ["Declared & Verified", "Declared, Pending Verification", "Not Declared"])
    with c3:
        pep_status               = st.selectbox("🏛️ PEP Status",              ["Not a PEP", "PEP – Domestic", "PEP – Foreign", "Close Associate of PEP"])
        adverse_media            = st.selectbox("📰 Adverse Media / Sanctions",["Clear", "Minor Flag (Explainable)", "Significant Flag", "On Watchlist / Sanctioned"])
        fatf_country             = st.selectbox("🌍 FATF Jurisdiction Risk",  ["Low Risk (FATF Compliant)", "Medium Risk", "High Risk (FATF Grey List)", "Prohibited (FATF Black List)"])

    c1, c2 = st.columns(2)
    with c1:
        source_consistency = st.selectbox("🔄 Source of Funds Consistency", ["Fully Consistent", "Minor Variance (Explainable)", "Significant Unexplained Variance"])
    with c2:
        unusual_txn        = st.selectbox("⚠️ Unusual Transaction Patterns", ["None Observed", "Minor – Under Review", "Suspicious – SAR Filed"])

    st.divider()

    # ── Section 3: Risk Profile ──────────────────────────────────────────────
    st.markdown("#### 📊 Section 3 — Investor Risk Profile & Suitability")
    c1, c2, c3 = st.columns(3)
    with c1:
        risk_appetite            = st.selectbox("📊 Risk Tolerance",          ["Conservative", "Moderate", "Aggressive", "Very Aggressive"])
        inv_experience_yrs       = st.slider("📅 Investment Experience (Yrs)", 0, 40, 5)
        prior_aif_pms            = st.selectbox("📁 Prior AIF / PMS",         ["None", "PMS Only", "Category I AIF", "Category II AIF", "Category III AIF", "Multiple AIFs"])
    with c2:
        inv_horizon              = st.selectbox("⏳ Investment Horizon",       ["< 1 Year", "1–3 Years", "3–5 Years", "5–7 Years", "> 7 Years"])
        liquidity_need           = st.selectbox("💧 Liquidity Requirement",    ["Very High (< 6 months)", "High (6–12 months)", "Moderate (1–3 years)", "Low (> 3 years)"])
        loss_bearing             = st.selectbox("📉 Can Sustain Capital Loss?",["Yes – Fully", "Yes – Partial (up to 30%)", "Limited (up to 10%)", "No"])
    with c3:
        financial_sophistication = st.selectbox("🎓 Financial Sophistication", ["Institutional / Family Office", "UHNI – Self-Managed", "HNI – Advised by Wealth Manager", "HNI – Limited Knowledge"])
        aif_category_interest    = st.selectbox("🏷️ AIF Category of Interest", ["Category I (Infra/VC/SME/Social)", "Category II (PE/Debt/Real Estate)", "Category III (Hedge / Long-Short)"])

    if st.button("🔍 **RUN COMPLETE AIF ELIGIBILITY CHECK**", type="primary", use_container_width=True):

        # ── Financial eligibility checks ───────────────────────────────────
        fin_issues = []
        if investment_cr < 1.0:          fin_issues.append("Investment < ₹1 Cr (SEBI Reg. 10 minimum)")
        if annual_income_lakhs < 40:     fin_issues.append("Annual Income < ₹40 Lakhs")
        if net_worth_cr < 5.0:           fin_issues.append("Net Worth < ₹5 Cr (preferred threshold)")
        if len(selected_blocked) > 0:    fin_issues.append(f"Blocked wealth source: {', '.join(selected_blocked)}")

        # ── KYC/AML checks ─────────────────────────────────────────────────
        kyc_issues = []
        if pan_verified != "Verified with ITD":              kyc_issues.append("PAN not verified with Income Tax Department")
        if aadhaar_verified == "Not Submitted":              kyc_issues.append("Aadhaar / OVD not submitted")
        if cvl_kyc != "KYC Compliant":                      kyc_issues.append("CVL/KRA KYC not compliant")
        if pep_status in ["PEP – Foreign", "Close Associate of PEP"]: kyc_issues.append(f"Elevated PEP risk: {pep_status}")
        if adverse_media in ["Significant Flag", "On Watchlist / Sanctioned"]: kyc_issues.append(f"Adverse media: {adverse_media}")
        if fatf_country in ["High Risk (FATF Grey List)", "Prohibited (FATF Black List)"]: kyc_issues.append(f"High-risk jurisdiction: {fatf_country}")
        if ubo_declared != "Declared & Verified":            kyc_issues.append("UBO declaration incomplete")
        if source_consistency == "Significant Unexplained Variance": kyc_issues.append("Significant unexplained variance in source of funds")
        if unusual_txn == "Suspicious – SAR Filed":          kyc_issues.append("Suspicious activity report (SAR) filed")

        # ── Risk profile scoring ────────────────────────────────────────────
        rp_score = 0
        rp_score += {"Conservative": 5, "Moderate": 10, "Aggressive": 18, "Very Aggressive": 25}[risk_appetite]
        rp_score += min(15, inv_experience_yrs * 0.75)
        rp_score += {"None": 0, "PMS Only": 5, "Category I AIF": 8, "Category II AIF": 10, "Category III AIF": 12, "Multiple AIFs": 15}[prior_aif_pms]
        rp_score += {"< 1 Year": 2, "1–3 Years": 5, "3–5 Years": 10, "5–7 Years": 14, "> 7 Years": 18}[inv_horizon]
        rp_score += {"Very High (< 6 months)": 2, "High (6–12 months)": 5, "Moderate (1–3 years)": 10, "Low (> 3 years)": 15}[liquidity_need]
        rp_score += {"Yes – Fully": 12, "Yes – Partial (up to 30%)": 8, "Limited (up to 10%)": 4, "No": 0}[loss_bearing]
        rp_score = min(100, rp_score)

        rp_band = ("Aggressive Investor" if rp_score >= 75
                   else "Growth Investor" if rp_score >= 55
                   else "Balanced Investor" if rp_score >= 35
                   else "Conservative Investor")

        # ── Category suitability map ────────────────────────────────────────
        suitable_categories = []
        if rp_score >= 35: suitable_categories.append("Category I (Infra/VC/SME/Social)")
        if rp_score >= 55: suitable_categories.append("Category II (PE/Debt/Real Estate)")
        if rp_score >= 75: suitable_categories.append("Category III (Hedge / Long-Short)")
        category_suitable = aif_category_interest in suitable_categories

        rp_issues = []
        if not category_suitable:
            rp_issues.append(f"{aif_category_interest} requires higher risk tolerance (current score {rp_score:.0f}/100)")
        if liquidity_need in ["Very High (< 6 months)", "High (6–12 months)"] and inv_horizon in ["< 1 Year", "1–3 Years"]:
            rp_issues.append("Short horizon + high liquidity need misaligned with AIF lock-in structure")
        if financial_sophistication == "HNI – Limited Knowledge" and "Category III" in aif_category_interest:
            rp_issues.append("Limited financial sophistication for Category III complex products")

        all_issues = fin_issues + kyc_issues + rp_issues
        aml_hard_block = any(x in " ".join(kyc_issues) for x in ["Watchlist", "SAR", "Prohibited"])
        blocked_source_hit = len(selected_blocked) > 0

        if aml_hard_block or blocked_source_hit:
            overall_status = "HARD REJECT"
            overall_color  = "#7f1d1d"; overall_bg = "#fef2f2"; overall_border = "#dc2626"
            overall_icon   = "🚫"
        elif len(all_issues) == 0:
            overall_status = "ELIGIBLE — PROCEED TO ONBOARDING"
            overall_color  = "#0f4c2a"; overall_bg = "#f0fdf4"; overall_border = "#059669"
            overall_icon   = "✅"
        elif len(all_issues) <= 2:
            overall_status = "CONDITIONALLY ELIGIBLE — EXCEPTIONS NOTED"
            overall_color  = "#7c3a00"; overall_bg = "#fffbeb"; overall_border = "#d97706"
            overall_icon   = "⚠️"
        else:
            overall_status = "NOT ELIGIBLE — MATERIAL DEFICIENCIES"
            overall_color  = "#7f1d1d"; overall_bg = "#fef2f2"; overall_border = "#dc2626"
            overall_icon   = "❌"

        def abadge(ok, hard=False):
            if ok:
                return "<span style='background:#059669;color:white;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:600;'>✔ PASS</span>"
            if hard:
                return "<span style='background:#7f1d1d;color:white;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:600;'>⛔ BLOCK</span>"
            return "<span style='background:#dc2626;color:white;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:600;'>✘ FAIL</span>"

        def rp_bar(score):
            pct = min(100, score)
            color = "#059669" if pct >= 75 else "#0284c7" if pct >= 55 else "#d97706" if pct >= 35 else "#dc2626"
            return f"<div style='background:#e2e8f0;border-radius:6px;height:10px;'><div style='background:{color};width:{pct:.0f}%;height:10px;border-radius:6px;'></div></div>"

        fin_rows = "".join(f"""<tr style='border-bottom:1px solid #e2e8f0;'>
            <td style='padding:10px 14px;font-weight:500;color:#1e293b;'>{n}</td>
            <td style='padding:10px 14px;color:#475569;font-size:0.9rem;'>{v}</td>
            <td style='padding:10px 14px;text-align:center;'>{abadge(ok)}</td></tr>"""
            for n, v, ok in [
                ("Minimum Investment",    f"₹{investment_cr:,.2f} Cr (Floor ₹1 Cr)",          investment_cr >= 1.0),
                ("Annual Income",         f"₹{annual_income_lakhs:,.1f} L (Floor ₹40 L)",      annual_income_lakhs >= 40),
                ("Net Worth",             f"₹{net_worth_cr:,.1f} Cr (Preferred ≥ ₹5 Cr)",     net_worth_cr >= 5.0),
                ("Liquid Assets",         f"₹{liquid_assets_cr:,.1f} Cr",                       liquid_assets_cr >= 1.0),
                ("Source of Wealth",      income_source,                                          len(selected_blocked) == 0),
            ])

        kyc_rows = "".join(f"""<tr style='border-bottom:1px solid #e2e8f0;'>
            <td style='padding:10px 14px;font-weight:500;color:#1e293b;'>{n}</td>
            <td style='padding:10px 14px;color:#475569;font-size:0.9rem;'>{v}</td>
            <td style='padding:10px 14px;text-align:center;'>{abadge(ok, hb)}</td></tr>"""
            for n, v, ok, hb in [
                ("PAN Verification",        pan_verified,      pan_verified == "Verified with ITD",                                   False),
                ("Aadhaar / OVD",           aadhaar_verified,  aadhaar_verified != "Not Submitted",                                   False),
                ("CVL / KRA KYC",           cvl_kyc,           cvl_kyc == "KYC Compliant",                                            False),
                ("Demat Account",           demat_account,     demat_account.startswith("Active"),                                     False),
                ("PEP Status",              pep_status,        pep_status not in ["PEP – Foreign","Close Associate of PEP"],           pep_status == "PEP – Foreign"),
                ("Adverse Media / Sanctions", adverse_media,   adverse_media == "Clear",                                              "Watchlist" in adverse_media or "Sanctioned" in adverse_media),
                ("FATF Jurisdiction",       fatf_country,      fatf_country not in ["High Risk (FATF Grey List)","Prohibited (FATF Black List)"], "Prohibited" in fatf_country),
                ("UBO Declaration",         ubo_declared,      ubo_declared == "Declared & Verified",                                 False),
                ("Source of Funds Consistency", source_consistency, source_consistency != "Significant Unexplained Variance",         False),
                ("Unusual Transactions",    unusual_txn,       unusual_txn == "None Observed",                                       "SAR" in unusual_txn),
            ])

        rp_rows = "".join(f"""<tr style='border-bottom:1px solid #e2e8f0;'>
            <td style='padding:10px 14px;font-weight:500;color:#1e293b;'>{n}</td>
            <td style='padding:10px 14px;color:#475569;font-size:0.9rem;'>{v}</td></tr>"""
            for n, v in [
                ("Risk Tolerance",          risk_appetite),
                ("Investment Experience",   f"{inv_experience_yrs} years"),
                ("Prior AIF / PMS",         prior_aif_pms),
                ("Investment Horizon",      inv_horizon),
                ("Liquidity Requirement",   liquidity_need),
                ("Loss-Bearing Capacity",   loss_bearing),
                ("Financial Sophistication",financial_sophistication),
                ("AIF Category Interest",   aif_category_interest),
                ("Category Suitability",    "✔ Suitable" if category_suitable else "✘ Mismatch with risk score"),
            ])

        st.markdown(f"""
        <div style='border:1px solid #e2e8f0;border-radius:16px;overflow:hidden;margin-top:1.5rem;font-family:Inter,sans-serif;'>

          <!-- Header -->
          <div style='background:linear-gradient(135deg,#1e293b,#312e81);padding:1.6rem 2rem;display:flex;justify-content:space-between;align-items:center;'>
            <div>
              <span style='color:#a5b4fc;font-size:0.78rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;'>KFintech — SEBI Registered Investment Manager</span>
              <h2 style='color:white;margin:4px 0 0 0;font-size:1.5rem;font-weight:700;'>AIF Investor Eligibility Report</h2>
            </div>
            <span style='background:rgba(255,255,255,0.15);color:white;padding:6px 16px;border-radius:20px;font-size:0.82rem;font-weight:600;'>
              SEBI AIF Reg. 2012 · {pd.Timestamp.now().strftime("%d %b %Y")}
            </span>
          </div>

          <!-- Overall Status Banner -->
          <div style='background:{overall_bg};border-left:5px solid {overall_border};padding:1.2rem 2rem;'>
            <p style='color:{overall_color};font-size:1.15rem;font-weight:800;margin:0;'>{overall_icon} {overall_status}</p>
            <p style='color:{overall_color};font-size:0.88rem;margin:4px 0 0 0;opacity:0.85;'>
              Financial Issues: {len(fin_issues)} &nbsp;|&nbsp; KYC/AML Flags: {len(kyc_issues)} &nbsp;|&nbsp; Risk Profile Issues: {len(rp_issues)} &nbsp;|&nbsp; Total Deviations: {len(all_issues)}
            </p>
          </div>

          <!-- Section 1: Financial Eligibility -->
          <div style='padding:1.4rem 2rem;border-bottom:1px solid #e2e8f0;'>
            <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 12px 0;'>Section 1 — Financial Eligibility (SEBI Accreditation Criteria)</p>
            <table style='width:100%;border-collapse:collapse;font-size:0.88rem;'>
              <thead><tr style='background:#f1f5f9;'>
                <th style='padding:10px 14px;text-align:left;color:#475569;font-weight:600;'>Parameter</th>
                <th style='padding:10px 14px;text-align:left;color:#475569;font-weight:600;'>Value</th>
                <th style='padding:10px 14px;text-align:center;color:#475569;font-weight:600;'>Status</th>
              </tr></thead>
              <tbody>{fin_rows}</tbody>
            </table>
          </div>

          <!-- Section 2: KYC / AML -->
          <div style='padding:1.4rem 2rem;border-bottom:1px solid #e2e8f0;'>
            <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 12px 0;'>Section 2 — KYC / AML & Sanctions Compliance</p>
            <table style='width:100%;border-collapse:collapse;font-size:0.88rem;'>
              <thead><tr style='background:#f1f5f9;'>
                <th style='padding:10px 14px;text-align:left;color:#475569;font-weight:600;'>Control</th>
                <th style='padding:10px 14px;text-align:left;color:#475569;font-weight:600;'>Declared Value</th>
                <th style='padding:10px 14px;text-align:center;color:#475569;font-weight:600;'>Status</th>
              </tr></thead>
              <tbody>{kyc_rows}</tbody>
            </table>
          </div>

          <!-- Section 3: Risk Profile -->
          <div style='padding:1.4rem 2rem;border-bottom:1px solid #e2e8f0;'>
            <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 14px 0;'>Section 3 — Investor Risk Profile & Suitability Assessment</p>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;'>
              <table style='border-collapse:collapse;font-size:0.88rem;'>
                <tbody>{rp_rows}</tbody>
              </table>
              <div>
                <div style='background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:1rem;'>
                  <p style='color:#64748b;font-size:0.75rem;margin:0 0 4px 0;text-transform:uppercase;letter-spacing:0.08em;'>Risk Score</p>
                  <p style='color:#1e293b;font-size:2rem;font-weight:800;margin:0;'>{rp_score:.0f}<span style='font-size:1rem;font-weight:400;color:#64748b;'>/100</span></p>
                  <p style='color:#3b82f6;font-size:0.88rem;font-weight:600;margin:6px 0 8px 0;'>{rp_band}</p>
                  {rp_bar(rp_score)}
                </div>
                <div style='background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.2rem 1.5rem;'>
                  <p style='color:#64748b;font-size:0.75rem;margin:0 0 8px 0;text-transform:uppercase;letter-spacing:0.08em;'>Suitable AIF Categories</p>
                  {"".join(f"<p style='color:#059669;font-size:0.85rem;font-weight:600;margin:3px 0;'>✔ {c}</p>" for c in suitable_categories) if suitable_categories else "<p style='color:#dc2626;font-size:0.85rem;'>No category suitable at current risk level</p>"}
                </div>
              </div>
            </div>
          </div>

          <!-- Section 4: Recommendation -->
          <div style='padding:1.6rem 2rem;background:{overall_bg};border-left:5px solid {overall_border};'>
            <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 6px 0;'>Compliance Officer Recommendation</p>
            <p style='color:{overall_color};font-size:1.05rem;font-weight:700;margin:0 0 8px 0;'>{overall_icon} {overall_status}</p>
            <p style='color:{overall_color};font-size:0.9rem;margin:0;line-height:1.65;'>
              {"All SEBI accreditation criteria, KYC/AML controls, and risk suitability benchmarks are satisfactorily met. The investor may be onboarded upon receipt of signed subscription agreement, KYC dossier, and Board/trustee approval per SEBI AIF Regulations 2012." if len(all_issues) == 0 and not aml_hard_block
               else "Hard-block triggers detected (sanctions / SAR / prohibited jurisdiction / blocked wealth source). Onboarding must be halted immediately. Refer to Compliance & Legal team. Mandatory SAR filing review required under PMLA 2002." if aml_hard_block or blocked_source_hit
               else f"The investor profile has {len(all_issues)} open deviation(s). Conditional onboarding may proceed post-exception approval by the Investment Committee, subject to resolution of flagged items. Enhanced Due Diligence (EDD) mandatory where KYC/AML flags are present." if len(all_issues) <= 2
               else "Multiple material deficiencies exist across financial eligibility, KYC/AML compliance, and/or risk suitability dimensions. Onboarding cannot proceed. Investor may reapply upon resolution of all flagged deviations with fresh documentation."}
            </p>
          </div>

        </div>
        """, unsafe_allow_html=True)

# === 3. TERM INSURANCE - FULL HEALTH PROFILE RESTORED ===
elif product == "🛡️ Term Insurance":
    st.markdown('<div class="product-card"><h2>🛡️ Term Insurance Premium Calculator (Complete Health Profile)</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.slider("👤 Age", 18, 65, 35)
        cover_amount_cr = st.selectbox("💰 Sum Assured (₹ Cr)", [0.25, 0.5, 1.0, 2.0, 5.0])
        policy_term = st.slider("📅 Policy Term (Years)", 10, 40, 20)
    with col2:
        smoker_status = st.radio("🚬 Smoking Status", ["Non-Smoker", "Smoker"])
        alcohol_status = st.radio("🍺 Alcohol Consumption", ["None", "Social", "Regular", "Heavy"])
    with col3:
        health_rating = st.selectbox("🏥 Self-Reported Health", ["Excellent", "Good", "Average", "Poor"])
    
    # FULL MEDICAL HISTORY
    st.subheader("🩺 **Medical History**")
    medical_conditions = st.multiselect("Existing Conditions", [
        "Diabetes", "Hypertension", "Heart Disease", "Cancer History", 
        "Stroke", "Kidney Issues", "Liver Disease", "None"
    ])
    
    if st.button("🛡️ **CALCULATE RISK-ADJUSTED PREMIUM**", type="primary", use_container_width=True):
        # ── Risk model ───────────────────────────────────────────────────────
        base_rate_clean = 0.0008 + (age - 30) * 0.00005

        smoking_load   = 2.2  if smoker_status == "Smoker" else 1.0
        alcohol_load   = 1.8  if alcohol_status == "Heavy" else 1.4 if alcohol_status == "Regular" else 1.1 if alcohol_status == "Social" else 1.0
        health_load    = 2.0  if health_rating == "Poor"   else 1.5 if health_rating == "Average" else 1.0
        diabetes_load  = 1.6  if "Diabetes"      in medical_conditions else 1.0
        heart_load     = 2.5  if "Heart Disease"  in medical_conditions else 1.0
        cancer_load    = 3.0  if "Cancer History" in medical_conditions else 1.0
        hyper_load     = 1.3  if "Hypertension"   in medical_conditions else 1.0
        stroke_load    = 2.0  if "Stroke"          in medical_conditions else 1.0
        kidney_load    = 1.8  if "Kidney Issues"   in medical_conditions else 1.0
        liver_load     = 1.7  if "Liver Disease"   in medical_conditions else 1.0

        base_rate = base_rate_clean * smoking_load * alcohol_load * health_load
        base_rate *= diabetes_load * heart_load * cancer_load * hyper_load * stroke_load * kidney_load * liver_load

        cover_amount   = cover_amount_cr * 10_000_000
        annual_premium = cover_amount * base_rate
        total_premium  = annual_premium * policy_term
        loading_pct    = (base_rate / base_rate_clean - 1) * 100
        loading_mult   = base_rate / base_rate_clean

        if base_rate < 0.0015:
            decision = "STANDARD ISSUANCE"; d_color = "#0f4c2a"; d_bg = "#f0fdf4"; d_border = "#059669"; d_icon = "✅"
            d_note = "Risk profile is within standard mortality assumptions. Policy may be issued at quoted premium without additional exclusions."
        elif base_rate < 0.003:
            decision = "ISSUANCE WITH LOADING"; d_color = "#7c3a00"; d_bg = "#fffbeb"; d_border = "#d97706"; d_icon = "⚠️"
            d_note = "Elevated risk due to lifestyle or health factors. Policy issuable subject to extra premium loading and applicable exclusion clauses on declared conditions."
        else:
            decision = "DECLINED / REFER TO REINSURER"; d_color = "#7f1d1d"; d_bg = "#fef2f2"; d_border = "#dc2626"; d_icon = "🚫"
            d_note = "Aggregate risk loading exceeds standard underwriting limits. Proposal declined at current health/lifestyle profile. May be reconsidered via reinsurer facultative placement or after material health improvement."

        def ti_badge(ok):
            return ("<span style='background:#059669;color:white;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:600;'>✔ Standard</span>"
                    if ok else
                    "<span style='background:#dc2626;color:white;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:600;'>⚠ Loaded</span>")

        def load_bar(load_factor):
            pct = min(100, (load_factor - 1) * 50)
            color = "#059669" if load_factor <= 1.0 else "#d97706" if load_factor <= 2.0 else "#dc2626"
            return f"<div style='background:#e2e8f0;border-radius:6px;height:8px;'><div style='background:{color};width:{max(4,pct):.0f}%;height:8px;border-radius:6px;'></div></div>"

        risk_rows = "".join(
            f"""<tr style='border-bottom:1px solid #e2e8f0;'>
                  <td style='padding:9px 14px;font-weight:500;color:#1e293b;font-size:0.88rem;'>{factor}</td>
                  <td style='padding:9px 14px;color:#475569;font-size:0.88rem;'>{declared}</td>
                  <td style='padding:9px 14px;text-align:center;font-weight:600;color:#1e40af;font-size:0.88rem;'>{load:.2f}x</td>
                  <td style='padding:9px 14px;width:160px;'>{load_bar(load)}</td>
                  <td style='padding:9px 14px;text-align:center;'>{ti_badge(load <= 1.0)}</td>
               </tr>"""
            for factor, declared, load in [
                ("Age Mortality Base",     f"{age} years",                        base_rate_clean / 0.0008),
                ("Smoking Status",         smoker_status,                          smoking_load),
                ("Alcohol Consumption",    alcohol_status,                         alcohol_load),
                ("Self-Reported Health",   health_rating,                          health_load),
                ("Diabetes",               "Present" if "Diabetes"      in medical_conditions else "None", diabetes_load),
                ("Heart Disease",          "Present" if "Heart Disease"  in medical_conditions else "None", heart_load),
                ("Cancer History",         "Present" if "Cancer History" in medical_conditions else "None", cancer_load),
                ("Hypertension",           "Present" if "Hypertension"   in medical_conditions else "None", hyper_load),
                ("Stroke",                 "Present" if "Stroke"          in medical_conditions else "None", stroke_load),
                ("Kidney Issues",          "Present" if "Kidney Issues"   in medical_conditions else "None", kidney_load),
                ("Liver Disease",          "Present" if "Liver Disease"   in medical_conditions else "None", liver_load),
            ]
        )

        st.markdown(f"""
        <div style='border:1px solid #e2e8f0;border-radius:16px;overflow:hidden;margin-top:1.5rem;font-family:Inter,sans-serif;'>

          <!-- Report Header -->
          <div style='background:linear-gradient(135deg,#1e293b,#065f46);padding:1.6rem 2rem;display:flex;justify-content:space-between;align-items:center;'>
            <div>
              <span style='color:#6ee7b7;font-size:0.78rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;'>KFintech — IRDAI Regulated Life Insurance Division</span>
              <h2 style='color:white;margin:4px 0 0 0;font-size:1.5rem;font-weight:700;'>Term Insurance Underwriting Assessment</h2>
            </div>
            <span style='background:rgba(255,255,255,0.15);color:white;padding:6px 16px;border-radius:20px;font-size:0.82rem;font-weight:600;'>
              IRDAI Compliant · {pd.Timestamp.now().strftime("%d %b %Y")}
            </span>
          </div>

          <!-- Decision Banner -->
          <div style='background:{d_bg};border-left:5px solid {d_border};padding:1.2rem 2rem;'>
            <p style='color:{d_color};font-size:1.15rem;font-weight:800;margin:0;'>{d_icon} {decision}</p>
            <p style='color:{d_color};font-size:0.88rem;margin:6px 0 0 0;line-height:1.6;opacity:0.9;'>{d_note}</p>
          </div>

          <!-- KPI Strip -->
          <div style='display:grid;grid-template-columns:repeat(5,1fr);border-bottom:1px solid #e2e8f0;'>
            {"".join(f"<div style='padding:1.1rem 1.4rem;border-right:1px solid #e2e8f0;'><p style='color:#64748b;font-size:0.75rem;margin:0 0 4px 0;text-transform:uppercase;letter-spacing:0.06em;'>{lbl}</p><p style='color:#1e293b;font-size:1.25rem;font-weight:700;margin:0;'>{val}</p></div>" for lbl, val in [
                ("Insured Age",         f"{age} yrs"),
                ("Sum Assured",         f"₹{cover_amount_cr} Cr"),
                ("Policy Term",         f"{policy_term} yrs"),
                ("Annual Premium",      f"₹{annual_premium:,.0f}"),
                ("Total Outgo",         f"₹{total_premium:,.0f}"),
            ])}
          </div>

          <!-- Risk Loading Summary -->
          <div style='display:grid;grid-template-columns:1fr 1fr;border-bottom:1px solid #e2e8f0;'>
            <div style='padding:1.2rem 1.6rem;border-right:1px solid #e2e8f0;'>
              <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 10px 0;'>Premium Derivation</p>
              <table style='width:100%;border-collapse:collapse;font-size:0.88rem;'>
                <tr><td style='color:#64748b;padding:4px 0;'>Base Mortality Rate</td><td style='color:#1e293b;font-weight:600;text-align:right;'>{base_rate_clean*1000:.3f}‰</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Loaded Mortality Rate</td><td style='color:#dc2626;font-weight:700;text-align:right;'>{base_rate*1000:.3f}‰</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Aggregate Risk Multiplier</td><td style='color:#1e40af;font-weight:700;text-align:right;'>{loading_mult:.2f}x</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Extra Premium Loading</td><td style='color:#dc2626;font-weight:700;text-align:right;'>+{loading_pct:.0f}%</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Annual Premium</td><td style='color:#059669;font-weight:700;text-align:right;'>₹{annual_premium:,.0f}</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Total Premium ({policy_term} yrs)</td><td style='color:#059669;font-weight:700;text-align:right;'>₹{total_premium:,.0f}</td></tr>
              </table>
            </div>
            <div style='padding:1.2rem 1.6rem;'>
              <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 10px 0;'>Applicant Health Snapshot</p>
              <table style='width:100%;border-collapse:collapse;font-size:0.88rem;'>
                <tr><td style='color:#64748b;padding:4px 0;'>Age Band</td><td style='color:#1e293b;font-weight:600;text-align:right;'>{"18–35 (Preferred)" if age <= 35 else "36–45 (Standard)" if age <= 45 else "46–55 (Rated)" if age <= 55 else "56–65 (High Risk)"}</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Smoking Status</td><td style='color:#1e293b;font-weight:600;text-align:right;'>{smoker_status}</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Alcohol Consumption</td><td style='color:#1e293b;font-weight:600;text-align:right;'>{alcohol_status}</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Self-Reported Health</td><td style='color:#1e293b;font-weight:600;text-align:right;'>{health_rating}</td></tr>
                <tr><td style='color:#64748b;padding:4px 0;'>Medical Conditions</td><td style='color:#{"dc2626" if medical_conditions and "None" not in medical_conditions else "059669"};font-weight:600;text-align:right;'>{", ".join([c for c in medical_conditions if c != "None"]) or "None Declared"}</td></tr>
              </table>
            </div>
          </div>

          <!-- Risk Factor Breakdown -->
          <div style='padding:1.4rem 2rem;border-bottom:1px solid #e2e8f0;'>
            <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 12px 0;'>Risk Factor Loading Breakdown</p>
            <table style='width:100%;border-collapse:collapse;font-size:0.88rem;'>
              <thead><tr style='background:#f1f5f9;'>
                <th style='padding:10px 14px;text-align:left;color:#475569;font-weight:600;'>Risk Factor</th>
                <th style='padding:10px 14px;text-align:left;color:#475569;font-weight:600;'>Declared</th>
                <th style='padding:10px 14px;text-align:center;color:#475569;font-weight:600;'>Loading</th>
                <th style='padding:10px 14px;text-align:left;color:#475569;font-weight:600;'>Intensity</th>
                <th style='padding:10px 14px;text-align:center;color:#475569;font-weight:600;'>Rating</th>
              </tr></thead>
              <tbody>{risk_rows}</tbody>
            </table>
          </div>

          <!-- Underwriter Note -->
          <div style='padding:1.4rem 2rem;background:#f8fafc;'>
            <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 6px 0;'>Underwriter Notes & Conditions</p>
            <p style='color:#334155;font-size:0.88rem;margin:0;line-height:1.7;'>
              {"<strong>No exclusion clauses required.</strong> Standard policy terms apply. Medical examination waived for sum assured ≤ ₹50 Lakhs per IRDAI guidelines. Nominee and premium payment mode to be confirmed at policy issuance." if loading_mult < 2
               else f"<strong>Extra premium of +{loading_pct:.0f}% applied.</strong> The following conditions are noted for exclusion or waiting period: {', '.join([c for c in medical_conditions if c != 'None']) or 'lifestyle risk factors'}. Full medical examination (including ECG, blood panel, and specialist report) mandatory prior to policy issuance. Exclusion clauses to be incorporated in policy schedule." if loading_mult < 5
               else "<strong>Proposal declined under standard underwriting parameters.</strong> Aggregate mortality loading is exceptionally high due to concurrent medical conditions. Options: (1) Refer to reinsurer for facultative underwriting; (2) Reduce sum assured to ₹25 Lakhs max; (3) Applicant may reapply following demonstrated health improvement with fresh medical reports."}
            </p>
          </div>

        </div>
        """, unsafe_allow_html=True)

# === 4. MF SIP CALCULATOR ===
elif product == "📈 MF SIP Calculator":
    st.markdown('<div class="product-card"><h2>📈 Mutual Fund SIP Calculator</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        monthly_sip = st.number_input("💰 Monthly SIP (₹)", 1000, 100000, 15000)
        investment_years = st.slider("📅 Period (Years)", 1, 30, 10)
    with col2:
        expected_returns = st.slider("📊 Annual Returns (%)", 8.0, 18.0, 12.0)
    
    if st.button("📈 **CALCULATE**", type="primary"):
        months = investment_years * 12
        monthly_rate = expected_returns / 12 / 100
        future_value = monthly_sip * ((1 + monthly_rate)**months - 1) / monthly_rate * (1 + monthly_rate)
        total_invested = monthly_sip * months
        
        col1, col2, col3 = st.columns(3)
        col1.metric("💎 Future Value", f"₹{future_value:,.0f}")
        col2.metric("💰 Total Invested", f"₹{total_invested:,.0f}")
        col3.metric("📈 Wealth Gain", f"₹{future_value-total_invested:,.0f}")

# === 5. EMI AMORTIZATION ===
elif product == "📊 EMI Amortization":
    st.markdown('<div class="product-card"><h2>📊 EMI Amortization Schedule Generator</h2></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        principal    = st.number_input("💰 Loan Amount (₹)", min_value=100000, max_value=100000000, value=2500000, step=50000)
    with c2:
        annual_rate  = st.slider("📊 Annual Interest Rate (%)", 6.0, 20.0, 8.5, 0.05)
    with c3:
        tenure_months = st.slider("📅 Tenure (Months)", 12, 360, 120)

    if st.button("📊 **GENERATE AMORTIZATION SCHEDULE**", type="primary", use_container_width=True):
        monthly_rate = annual_rate / 12 / 100
        emi = principal * monthly_rate * (1 + monthly_rate)**tenure_months / ((1 + monthly_rate)**tenure_months - 1)
        total_payment   = emi * tenure_months
        total_interest  = total_payment - principal
        interest_ratio  = (total_interest / principal) * 100

        # ── Build full schedule ──────────────────────────────────────────────
        schedule = []
        balance  = principal
        cumulative_principal = 0
        cumulative_interest  = 0
        for month in range(1, tenure_months + 1):
            interest_comp  = balance * monthly_rate
            principal_comp = emi - interest_comp
            balance        = max(0, balance - principal_comp)
            cumulative_principal += principal_comp
            cumulative_interest  += interest_comp
            schedule.append({
                "Month": month,
                "EMI (₹)":               round(emi, 0),
                "Principal (₹)":         round(principal_comp, 0),
                "Interest (₹)":          round(interest_comp, 0),
                "Cumulative Principal (₹)": round(cumulative_principal, 0),
                "Cumulative Interest (₹)":  round(cumulative_interest, 0),
                "Outstanding Balance (₹)":  round(balance, 0),
            })

        df_schedule = pd.DataFrame(schedule)

        # ── Summary report card ──────────────────────────────────────────────
        def amort_bar(pct):
            color = "#059669" if pct <= 30 else "#d97706" if pct <= 60 else "#dc2626"
            return f"<div style='background:#e2e8f0;border-radius:6px;height:10px;'><div style='background:{color};width:{min(100,pct):.0f}%;height:10px;border-radius:6px;'></div></div>"

        # Halfway balance (month at ~50% tenure)
        mid_row = df_schedule[df_schedule["Month"] == tenure_months // 2].iloc[0]

        st.markdown(f"""
        <div style='border:1px solid #e2e8f0;border-radius:16px;overflow:hidden;margin-top:1.5rem;font-family:Inter,sans-serif;'>

          <!-- Header -->
          <div style='background:linear-gradient(135deg,#1e293b,#1e3a8a);padding:1.6rem 2rem;display:flex;justify-content:space-between;align-items:center;'>
            <div>
              <span style='color:#93c5fd;font-size:0.78rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;'>KFintech — Loan Servicing Division</span>
              <h2 style='color:white;margin:4px 0 0 0;font-size:1.5rem;font-weight:700;'>EMI Amortization Report</h2>
            </div>
            <span style='background:rgba(255,255,255,0.15);color:white;padding:6px 16px;border-radius:20px;font-size:0.82rem;font-weight:600;'>
              {tenure_months} months · {annual_rate:.2f}% p.a. · {pd.Timestamp.now().strftime("%d %b %Y")}
            </span>
          </div>

          <!-- KPI Strip -->
          <div style='display:grid;grid-template-columns:repeat(5,1fr);border-bottom:1px solid #e2e8f0;'>
            {"".join(f"<div style='padding:1.1rem 1.4rem;border-right:1px solid #e2e8f0;'><p style='color:#64748b;font-size:0.73rem;margin:0 0 4px 0;text-transform:uppercase;letter-spacing:0.06em;'>{lbl}</p><p style='color:{col};font-size:1.2rem;font-weight:700;margin:0;'>{val}</p></div>" for lbl, val, col in [
                ("Loan Amount",      f"₹{principal:,.0f}",       "#1e293b"),
                ("Monthly EMI",      f"₹{emi:,.0f}",             "#1e40af"),
                ("Total Interest",   f"₹{total_interest:,.0f}",  "#dc2626"),
                ("Total Outflow",    f"₹{total_payment:,.0f}",   "#1e293b"),
                ("Interest Burden",  f"{interest_ratio:.1f}%",   "#dc2626" if interest_ratio > 50 else "#d97706" if interest_ratio > 25 else "#059669"),
            ])}
          </div>

          <!-- Cost of Credit Breakdown -->
          <div style='display:grid;grid-template-columns:1fr 1fr;border-bottom:1px solid #e2e8f0;'>
            <div style='padding:1.3rem 1.8rem;border-right:1px solid #e2e8f0;'>
              <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 12px 0;'>Cost of Credit Summary</p>
              <table style='width:100%;border-collapse:collapse;font-size:0.88rem;'>
                <tr><td style='color:#64748b;padding:5px 0;'>Principal Amount</td><td style='color:#1e293b;font-weight:600;text-align:right;'>₹{principal:,.0f}</td></tr>
                <tr><td style='color:#64748b;padding:5px 0;'>Total Interest Cost</td><td style='color:#dc2626;font-weight:700;text-align:right;'>₹{total_interest:,.0f}</td></tr>
                <tr><td style='color:#64748b;padding:5px 0;'>Total Amount Payable</td><td style='color:#1e293b;font-weight:700;text-align:right;'>₹{total_payment:,.0f}</td></tr>
                <tr><td style='color:#64748b;padding:5px 0;'>Interest-to-Principal Ratio</td><td style='color:#dc2626;font-weight:700;text-align:right;'>{interest_ratio:.1f}%</td></tr>
                <tr><td style='color:#64748b;padding:5px 0;'>Effective Monthly Rate</td><td style='color:#1e293b;font-weight:600;text-align:right;'>{monthly_rate*100:.4f}%</td></tr>
              </table>
            </div>
            <div style='padding:1.3rem 1.8rem;'>
              <p style='color:#64748b;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 12px 0;'>Mid-Tenure Snapshot (Month {tenure_months // 2})</p>
              <table style='width:100%;border-collapse:collapse;font-size:0.88rem;'>
                <tr><td style='color:#64748b;padding:5px 0;'>Outstanding Balance</td><td style='color:#1e40af;font-weight:700;text-align:right;'>₹{mid_row["Outstanding Balance (₹)"]:,.0f}</td></tr>
                <tr><td style='color:#64748b;padding:5px 0;'>Principal Repaid so far</td><td style='color:#059669;font-weight:600;text-align:right;'>₹{mid_row["Cumulative Principal (₹)"]:,.0f}</td></tr>
                <tr><td style='color:#64748b;padding:5px 0;'>Interest Paid so far</td><td style='color:#dc2626;font-weight:600;text-align:right;'>₹{mid_row["Cumulative Interest (₹)"]:,.0f}</td></tr>
                <tr><td style='color:#64748b;padding:5px 0;'>% Loan Repaid</td>
                    <td style='color:#1e293b;font-weight:600;text-align:right;'>{mid_row["Cumulative Principal (₹)"]/principal*100:.1f}%</td></tr>
              </table>
              <div style='margin-top:10px;'>
                <p style='color:#64748b;font-size:0.75rem;margin:0 0 4px 0;'>Principal Repaid at Midpoint</p>
                {amort_bar(mid_row["Cumulative Principal (₹)"]/principal*100)}
              </div>
            </div>
          </div>

        </div>
        """, unsafe_allow_html=True)

        # ── Full schedule table ──────────────────────────────────────────────
        st.markdown("#### 📋 Month-by-Month Amortization Schedule")

        # Format all money columns with ₹ and commas
        display_df = df_schedule.copy()
        for col_name in ["EMI (₹)", "Principal (₹)", "Interest (₹)",
                          "Cumulative Principal (₹)", "Cumulative Interest (₹)", "Outstanding Balance (₹)"]:
            display_df[col_name] = display_df[col_name].apply(lambda x: f"₹{x:,.0f}")

        st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)

# === FOOTER ===
st.markdown("""
<div style='background: linear-gradient(135deg, #1e293b, #1e40af); color: white; padding: 2.5rem; text-align: center; border-radius: 20px; margin-top: 3rem;'>
    <h3>KFintech Enterprise Financial Suite v7.2</h3>
    <p><strong>Madhu Kumar | AI Business Analyst | RBI/SEBI/IRDA Compliant</strong></p>
    <p>✅ FIXED Rejection Box | ✅ BLOCKED Sources Dropdown | ✅ Full Health Profile Restored</p>
</div>
""", unsafe_allow_html=True)
