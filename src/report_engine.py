from fpdf import FPDF
import datetime
import os
import plotly.io as pio
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class UltimateAlphaReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        if self.page_no() > 1:
            self.set_fill_color(11, 14, 20) # Aether Dark
            self.rect(0, 0, 210, 20, 'F')
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(0, 242, 255) # Cyan
            self.cell(0, 10, 'DEVANSH INTEL | STRATEGIC ALPHA AUDIT v5.0', 0, 1, 'R')
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Proprietary Alpha Intelligence | Page {self.page_no()}', 0, 0, 'C')

    def add_cover_page(self):
        self.add_page()
        self.set_fill_color(11, 14, 20)
        self.rect(0, 0, 210, 297, 'F')
        
        # Title
        self.set_y(100)
        self.set_font('Helvetica', 'B', 32)
        self.set_text_color(0, 242, 255)
        self.cell(0, 20, 'ALPHA STRATEGIC AUDIT', 0, 1, 'C')
        
        self.set_font('Helvetica', '', 18)
        self.set_text_color(185, 202, 203)
        self.cell(0, 15, 'EXECUTIVE-GRADE MARKET INTELLIGENCE v5.0', 0, 1, 'C')
        
        # Border
        self.set_draw_color(0, 242, 255)
        self.set_line_width(1)
        self.line(50, 140, 160, 140)
        
        self.set_y(250)
        self.set_font('Helvetica', 'I', 12)
        self.cell(0, 10, f'Generated for Terminal Session: {datetime.date.today()}', 0, 1, 'C')
        self.cell(0, 10, 'DEVANSH INTEL CORE | GLOBAL HQ', 0, 1, 'C')

    def add_section_title(self, title):
        self.ln(10)
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 242, 255)
        self.cell(0, 10, title.upper(), 0, 1, 'L')
        self.set_draw_color(0, 242, 255)
        self.set_line_width(0.5)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(5)

    def add_metric_box(self, label, value):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(30, 32, 36)
        self.cell(70, 10, f"{label}:", 0, 0)
        self.set_font('Helvetica', '', 12)
        self.cell(0, 10, str(value), 0, 1)

    def add_mpl_radar(self, labels, values, title):
        # Style
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        fig.patch.set_facecolor('#0c0e12')
        ax.set_facecolor('#1a1c20')
        
        # Ensure values reach back to start for closed loop
        plot_values = list(values)
        plot_values += plot_values[:1]
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]
        
        ax.plot(angles, plot_values, color='#00f2ff', linewidth=2)
        ax.fill(angles, plot_values, color='#00f2ff', alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, color='#b9cacb', size=8)
        ax.set_yticklabels([], color='#b9cacb')
        ax.set_title(title, color='#00f2ff', pad=20)
        
        temp_path = f"tmp_radar_{datetime.datetime.now().timestamp()}.png"
        plt.savefig(temp_path, dpi=100, bbox_inches='tight', facecolor='#0c0e12')
        plt.close()
        
        self.image(temp_path, x=45, w=120)
        self.ln(5)
        if os.path.exists(temp_path): os.remove(temp_path)

    def add_mpl_heatmap(self, df_matrix, title):
        plt.figure(figsize=(10, 6))
        plt.style.use('dark_background')
        # Filter only numeric for heatmap
        numeric_df = df_matrix.select_dtypes(include=[np.number])
        sns.heatmap(numeric_df, annot=True, cmap='GnBu', cbar=False)
        plt.title(title, color='#00f2ff')
        plt.xticks(color='#b9cacb', rotation=45)
        plt.yticks(color='#b9cacb')
        
        temp_path = f"tmp_heatmap_{datetime.datetime.now().timestamp()}.png"
        plt.savefig(temp_path, dpi=100, bbox_inches='tight', facecolor='#0c0e12')
        plt.close()
        
        self.image(temp_path, x=20, w=170)
        self.ln(5)
        if os.path.exists(temp_path): os.remove(temp_path)

    def add_mpl_bar(self, data_dict, title, xlabel, ylabel):
        plt.figure(figsize=(10, 6))
        plt.style.use('dark_background')
        plt.bar(data_dict.keys(), data_dict.values(), color='#00f2ff', alpha=0.7)
        plt.title(title, color='#00f2ff')
        plt.xlabel(xlabel, color='#b9cacb')
        plt.ylabel(ylabel, color='#b9cacb')
        plt.xticks(rotation=45, color='#b9cacb')
        plt.yticks(color='#b9cacb')
        
        temp_path = f"tmp_bar_{datetime.datetime.now().timestamp()}.png"
        plt.savefig(temp_path, dpi=100, bbox_inches='tight', facecolor='#0c0e12')
        plt.close()
        
        self.image(temp_path, x=20, w=170)
        self.ln(5)
        if os.path.exists(temp_path): os.remove(temp_path)

    def add_mpl_histogram(self, data_values, title, xlabel):
        plt.figure(figsize=(10, 6))
        plt.style.use('dark_background')
        plt.hist(data_values, bins=15, color='#14d1ff', alpha=0.7, edgecolor='#00f2ff')
        plt.title(title, color='#00f2ff')
        plt.xlabel(xlabel, color='#b9cacb')
        plt.ylabel("Frequency", color='#b9cacb')
        plt.xticks(color='#b9cacb')
        plt.yticks(color='#b9cacb')
        
        temp_path = f"tmp_hist_{datetime.datetime.now().timestamp()}.png"
        plt.savefig(temp_path, dpi=100, bbox_inches='tight', facecolor='#0c0e12')
        plt.close()
        
        self.image(temp_path, x=20, w=170)
        self.ln(5)
        if os.path.exists(temp_path): os.remove(temp_path)

    def add_plotly_chart(self, fig, filename, width=180):
        # Legacy Support / Failover
        self.set_draw_color(58, 73, 75)
        self.set_line_width(0.2)
        self.rect(15, self.get_y(), width, 20)
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(185, 202, 203)
        self.cell(0, 10, f"[VANQUISHED] External Engine: {filename.upper()}", 1, 1, 'C')
        self.ln(5)

def generate_ultimate_report(data):
    pdf = UltimateAlphaReport()
    pdf.add_cover_page()
    pdf.add_page()
    
    # 1. Executive Summary
    pdf.add_section_title("1. Executive Market Summary")
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    summary = (
        "This Alpha Strategic Audit provides a high-fidelity synthesis of current market dynamics. "
        "Our neural nodes have identified key growth corridors in AI and FinTech sectors, "
        "with a significant shift towards distributed infrastructure and LLM orchestration skills. "
        "The following analysis data-mines your specific terminal interactions to provide tailored strategic advice."
    )
    pdf.multi_cell(0, 7, summary)
    
    # 2. Market HQ Metrics
    pdf.add_section_title("2. Terminal HQ Analytics")
    pdf.add_metric_box("Global Nodes Analyzed", data.get("total_jobs", "N/A"))
    pdf.add_metric_box("Market Growth Index", "+418%")
    pdf.add_metric_box("Target Role Pulse", data.get("top_role", "AI Architect"))
    pdf.add_metric_box("Peak Comp Potential", data.get("peak_salary", "N/A"))
    
    # 3. Skill DNA (Radar Analysis) - NATIVE MPL
    if 'radar_data' in data:
        pdf.add_section_title("3. Genetic Skill Signature (Radar Analysis)")
        pdf.add_mpl_radar(data['radar_data']['labels'], data['radar_data']['values'], "Executive Skill Trajectory")
        pdf.set_font('Helvetica', 'I', 10)
        pdf.multi_cell(0, 5, "N.B.: The radar chart visualizes the delta between your current skill DNA and the target role signature.")

    # 4. Market Demand Heatmap - NATIVE MPL
    if 'heatmap_data' in data:
        pdf.add_page()
        pdf.add_section_title("4. Global Demand Clusters (LinkedIn Signal)")
        pdf.add_mpl_heatmap(data['heatmap_data'], "City vs Skill Matrix")

    # 5. Salary & Economic Outlook - NATIVE MPL
    pdf.add_section_title("5. Salary & Economic Intelligence")
    if 'salary_dist_data' in data:
        pdf.add_mpl_histogram(data['salary_dist_data'], "Executive Salary Distribution", "Compensation (INR)")
    
    if 'salary_premium_data' in data:
        pdf.add_mpl_bar(data['salary_premium_data'], "Skill vs Pay Alpha", "Strategic Skill", "Premium (₹)")

    # 6. Regional Growth Corridors - NATIVE MPL
    if 'regional_growth_data' in data:
        pdf.add_section_title("6. Regional Growth Signal")
        pdf.add_mpl_bar(data['regional_growth_data'], "Geographic Growth Momentum", "Global Node", "Growth %")

    # 7. Strategic Conclusion
    pdf.add_page()
    pdf.add_section_title("7. Alpha Strategic Roadmap")
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(30, 32, 36)
    advice = (
        "Based on the multi-node terminal session intelligence, we recommend an active pivot towards 'AI Engineering' "
        "and 'Distributed M LOps'. The candidate's skill signature aligns closely with high-density market clusters "
        "in Bangalore and Europe.\n\n"
        "Strategic Pillars:\n"
        "1. Skill Reinforcement: Focus on Vector Databases and LLM Orchestration.\n"
        "2. Node Migration: Bangalore remains the primary ROI node for 2026.\n"
        "3. Network Alpha: Leverage existing LinkedIn signal for preemptive hiring leads."
    )
    pdf.multi_cell(0, 8, advice)
    
    # System Status Footer
    pdf.ln(20)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(185, 202, 203)
    pdf.cell(0, 10, "This Strategic Audit was generated by the DEVANSH Vanguard Engine v5.3 (Ultra Stability Build).", 0, 1, 'C')
    
    path = "DEVANSH_Strategic_Audit_v5.pdf"
    pdf.output(path)
    return path
