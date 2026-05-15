import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("STATISTICAL ANALYSIS REPORT")
print("AI-Solutions Web Server Logs")
print("=" * 70)

# ============================================
# LOAD CLEANED DATA
# ============================================
print("\nLoading cleaned data...")

# Try to load cleaned data, if not found, generate sample
try:
    df = pd.read_csv("weblogs_cleaned.csv")
    print(f"Loaded {len(df):,} records from weblogs_cleaned.csv")
except FileNotFoundError:
    print("weblogs_cleaned.csv not found. Generating sample data...")
    np.random.seed(42)
    n = 10000
    df = pd.DataFrame({
        'lead_score': np.random.randint(0, 101, n),
        'satisfaction_score': np.random.choice([1,2,3,4,5], n, p=[0.05,0.1,0.2,0.35,0.3]),
        'response_time_ms': np.random.randint(50, 2000, n),
        'country': np.random.choice(['South Africa', 'Botswana', 'Namibia', 'Zimbabwe', 'Zambia'], n),
        'region': np.random.choice(['Southern Africa', 'East Africa', 'West Africa'], n),
        'conversion_flag': np.random.choice([True, False], n, p=[0.3, 0.7]),
        'ai_assistant_used': np.random.choice([True, False], n, p=[0.25, 0.75]),
        'timestamp': pd.date_range('2026-01-01', periods=n, freq='H')
    })
    print(f"Generated {len(df):,} sample records")

print(f"Columns: {len(df.columns)}")
print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")

# ============================================
# SECTION 1: MEASURES OF CENTRAL TENDENCY
# ============================================
print("\n" + "=" * 70)
print("SECTION 1: MEASURES OF CENTRAL TENDENCY")
print("=" * 70)

numerical_cols = ['lead_score', 'satisfaction_score', 'response_time_ms']
central_tendency_results = []

for col in numerical_cols:
    mean_val = df[col].mean()
    median_val = df[col].median()
    mode_val = df[col].mode().iloc[0] if not df[col].mode().empty else 0
    
    print(f"\n{col.upper()}:")
    print(f"   Mean (Average): {mean_val:.2f}")
    print(f"   Median (Middle): {median_val:.2f}")
    print(f"   Mode (Most Frequent): {mode_val}")
    print(f"   Skew: {(mean_val - median_val):.2f} ({'Right Skew' if mean_val > median_val else 'Left Skew' if mean_val < median_val else 'Symmetric'})")
    
    central_tendency_results.append({
        'Metric': col,
        'Mean': round(mean_val, 2),
        'Median': round(median_val, 2),
        'Mode': mode_val,
        'Skew Direction': 'Right Skew' if mean_val > median_val else 'Left Skew' if mean_val < median_val else 'Symmetric'
    })

# Create Central Tendency Table
fig_ct = go.Figure(data=[go.Table(
    header=dict(values=['Metric', 'Mean', 'Median', 'Mode', 'Skew Direction'],
                fill_color='#8B4513',
                font=dict(color='white', size=12),
                align='center'),
    cells=dict(values=[
        [r['Metric'] for r in central_tendency_results],
        [r['Mean'] for r in central_tendency_results],
        [r['Median'] for r in central_tendency_results],
        [r['Mode'] for r in central_tendency_results],
        [r['Skew Direction'] for r in central_tendency_results]
    ],
    fill_color='#F5F0E8',
    align='center')
)])
fig_ct.update_layout(title='<b>Table 1: Measures of Central Tendency</b>', 
                     height=300,
                     paper_bgcolor='#F5F0E8',
                     plot_bgcolor='#F5F0E8')
fig_ct.write_html("table_1_central_tendency.html")
print("\n[SAVED] table_1_central_tendency.html")

# ============================================
# SECTION 2: MEASURES OF DISPERSION
# ============================================
print("\n" + "=" * 70)
print("SECTION 2: MEASURES OF DISPERSION")
print("=" * 70)

dispersion_results = []

for col in numerical_cols:
    variance_val = df[col].var()
    std_val = df[col].std()
    range_val = df[col].max() - df[col].min()
    iqr_val = df[col].quantile(0.75) - df[col].quantile(0.25)
    
    print(f"\n{col.upper()}:")
    print(f"   Variance: {variance_val:.2f}")
    print(f"   Standard Deviation: {std_val:.2f}")
    print(f"   Range: {range_val:.2f}")
    print(f"   Interquartile Range (IQR): {iqr_val:.2f}")
    
    dispersion_results.append({
        'Metric': col,
        'Variance': round(variance_val, 2),
        'Std Deviation': round(std_val, 2),
        'Range': round(range_val, 2),
        'IQR': round(iqr_val, 2)
    })

fig_disp = go.Figure(data=[go.Table(
    header=dict(values=['Metric', 'Variance', 'Std Deviation', 'Range', 'IQR'],
                fill_color='#8B4513',
                font=dict(color='white', size=12),
                align='center'),
    cells=dict(values=[
        [r['Metric'] for r in dispersion_results],
        [r['Variance'] for r in dispersion_results],
        [r['Std Deviation'] for r in dispersion_results],
        [r['Range'] for r in dispersion_results],
        [r['IQR'] for r in dispersion_results]
    ],
    fill_color='#F5F0E8',
    align='center')
)])
fig_disp.update_layout(title='<b>Table 2: Measures of Dispersion</b>', 
                       height=300,
                       paper_bgcolor='#F5F0E8',
                       plot_bgcolor='#F5F0E8')
fig_disp.write_html("table_2_dispersion.html")
print("\n[SAVED] table_2_dispersion.html")

# ============================================
# SECTION 3: BOX PLOTS FOR OUTLIER DETECTION
# ============================================
print("\n" + "=" * 70)
print("SECTION 3: OUTLIER DETECTION - BOX PLOTS")
print("=" * 70)

fig_box1 = px.box(df, y='lead_score', title='<b>Box Plot: Lead Score Distribution</b>',
                  color_discrete_sequence=['#8B4513'])
fig_box1.update_layout(paper_bgcolor='#F5F0E8', 
                       plot_bgcolor='#F5F0E8',
                       yaxis_title='Lead Score (0-100)')
fig_box1.write_html("boxplot_lead_score.html")
print("  [SAVED] boxplot_lead_score.html")

fig_box2 = px.box(df, y='satisfaction_score', title='<b>Box Plot: Satisfaction Score Distribution</b>',
                  color_discrete_sequence=['#D2691E'])
fig_box2.update_layout(paper_bgcolor='#F5F0E8', 
                       plot_bgcolor='#F5F0E8',
                       yaxis_title='Satisfaction Score (1-5)')
fig_box2.write_html("boxplot_satisfaction.html")
print("  [SAVED] boxplot_satisfaction.html")

fig_box3 = px.box(df, y='response_time_ms', title='<b>Box Plot: Response Time Distribution</b>',
                  color_discrete_sequence=['#CD853F'])
fig_box3.update_layout(paper_bgcolor='#F5F0E8', 
                       plot_bgcolor='#F5F0E8',
                       yaxis_title='Response Time (ms)')
fig_box3.write_html("boxplot_response_time.html")
print("  [SAVED] boxplot_response_time.html")

fig_box_combined = make_subplots(rows=1, cols=3, 
                                 subplot_titles=('Lead Score', 'Satisfaction', 'Response Time'))

fig_box_combined.add_trace(go.Box(y=df['lead_score'], name='Lead Score', marker_color='#8B4513'), row=1, col=1)
fig_box_combined.add_trace(go.Box(y=df['satisfaction_score'], name='Satisfaction', marker_color='#D2691E'), row=1, col=2)
fig_box_combined.add_trace(go.Box(y=df['response_time_ms'], name='Response Time', marker_color='#CD853F'), row=1, col=3)

fig_box_combined.update_layout(title='<b>Box Plots: Outlier Detection Across Metrics</b>',
                               height=600,
                               paper_bgcolor='#F5F0E8',
                               plot_bgcolor='#F5F0E8',
                               showlegend=False)
fig_box_combined.write_html("boxplots_combined.html")
print("  [SAVED] boxplots_combined.html")

# ============================================
# SECTION 4: CORRELATION MATRIX
# ============================================
print("\n" + "=" * 70)
print("SECTION 4: CORRELATION MATRIX")
print("=" * 70)

correlation_cols = ['lead_score', 'satisfaction_score', 'response_time_ms']
corr_matrix = df[correlation_cols].corr()

print("\nPearson Correlation Matrix:")
print(corr_matrix.round(3))

fig_corr = px.imshow(corr_matrix, 
                     text_auto=True, 
                     aspect='auto',
                     color_continuous_scale=['#F5DEB3', '#D2691E', '#8B4513'],
                     title='<b>Correlation Matrix Heatmap</b>')
fig_corr.update_layout(paper_bgcolor='#F5F0E8',
                       plot_bgcolor='#F5F0E8',
                       height=500)
fig_corr.write_html("correlation_matrix.html")
print("\n[SAVED] correlation_matrix.html")

print("\nCorrelation Interpretations:")
corr_val = corr_matrix.loc['lead_score', 'satisfaction_score']
if corr_val > 0.5:
    corr_text = "Strong positive"
elif corr_val > 0.3:
    corr_text = "Moderate positive"
elif corr_val > 0:
    corr_text = "Weak positive"
else:
    corr_text = "Negative"
print(f"  - Lead Score vs Satisfaction: {corr_val:.3f} ({corr_text})")

resp_corr = corr_matrix.loc['response_time_ms', 'satisfaction_score']
if resp_corr < 0:
    print(f"  - Response Time vs Satisfaction: {resp_corr:.3f} (Faster responses lead to higher satisfaction)")
else:
    print(f"  - Response Time vs Satisfaction: {resp_corr:.3f} (Unexpected pattern)")

# ============================================
# SECTION 5: DISTRIBUTION HISTOGRAMS
# ============================================
print("\n" + "=" * 70)
print("SECTION 5: DISTRIBUTION HISTOGRAMS")
print("=" * 70)

fig_hist1 = px.histogram(df, x='lead_score', nbins=20, 
                         title='<b>Distribution: Lead Scores</b>',
                         color_discrete_sequence=['#8B4513'])
fig_hist1.update_layout(paper_bgcolor='#F5F0E8',
                        plot_bgcolor='#F5F0E8',
                        xaxis_title='Lead Score',
                        yaxis_title='Frequency')
fig_hist1.write_html("histogram_lead_score.html")
print("  [SAVED] histogram_lead_score.html")

fig_hist2 = px.histogram(df, x='satisfaction_score', nbins=5, 
                         title='<b>Distribution: Satisfaction Scores</b>',
                         color_discrete_sequence=['#D2691E'])
fig_hist2.update_layout(paper_bgcolor='#F5F0E8',
                        plot_bgcolor='#F5F0E8',
                        xaxis_title='Satisfaction Score (1-5)',
                        yaxis_title='Frequency')
fig_hist2.write_html("histogram_satisfaction.html")
print("  [SAVED] histogram_satisfaction.html")

fig_hist3 = px.histogram(df, x='response_time_ms', nbins=30, 
                         title='<b>Distribution: Response Times</b>',
                         color_discrete_sequence=['#CD853F'])
fig_hist3.update_layout(paper_bgcolor='#F5F0E8',
                        plot_bgcolor='#F5F0E8',
                        xaxis_title='Response Time (ms)',
                        yaxis_title='Frequency')
fig_hist3.write_html("histogram_response_time.html")
print("  [SAVED] histogram_response_time.html")

# ============================================
# SECTION 6: SCATTER PLOTS
# ============================================
print("\n" + "=" * 70)
print("SECTION 6: SCATTER PLOTS - RELATIONSHIPS")
print("=" * 70)

sample_df = df.sample(min(10000, len(df)))

fig_scatter1 = px.scatter(sample_df, x='response_time_ms', y='lead_score',
                         title='<b>Relationship: Response Time vs Lead Score</b>',
                         color='satisfaction_score',
                         color_continuous_scale=['#F5DEB3', '#D2691E', '#8B4513'],
                         opacity=0.6)
fig_scatter1.update_layout(paper_bgcolor='#F5F0E8',
                           plot_bgcolor='#F5F0E8',
                           xaxis_title='Response Time (ms)',
                           yaxis_title='Lead Score')
fig_scatter1.write_html("scatter_response_lead.html")
print("  [SAVED] scatter_response_lead.html")

fig_scatter2 = px.scatter(sample_df, x='lead_score', y='satisfaction_score',
                         title='<b>Relationship: Lead Score vs Satisfaction</b>',
                         color='response_time_ms',
                         color_continuous_scale=['#F5DEB3', '#D2691E', '#8B4513'],
                         opacity=0.6)
fig_scatter2.update_layout(paper_bgcolor='#F5F0E8',
                           plot_bgcolor='#F5F0E8',
                           xaxis_title='Lead Score',
                           yaxis_title='Satisfaction Score')
fig_scatter2.write_html("scatter_lead_satisfaction.html")
print("  [SAVED] scatter_lead_satisfaction.html")

# ============================================
# SECTION 7: CATEGORICAL ANALYSIS
# ============================================
print("\n" + "=" * 70)
print("SECTION 7: CATEGORICAL ANALYSIS")
print("=" * 70)

country_lead = df.groupby('country')['lead_score'].mean().sort_values(ascending=False).head(15).reset_index()
fig_bar1 = px.bar(country_lead, x='country', y='lead_score',
                  title='<b>Top 15 Countries by Average Lead Score</b>',
                  color='lead_score',
                  color_continuous_scale=['#F5DEB3', '#D2691E', '#8B4513'])
fig_bar1.update_layout(paper_bgcolor='#F5F0E8',
                       plot_bgcolor='#F5F0E8',
                       xaxis_title='Country',
                       yaxis_title='Average Lead Score')
fig_bar1.write_html("bar_country_lead.html")
print("  [SAVED] bar_country_lead.html")

region_conv = df.groupby('region')['conversion_flag'].mean().sort_values(ascending=False).reset_index()
fig_bar2 = px.bar(region_conv, x='region', y='conversion_flag',
                  title='<b>Conversion Rate by Region</b>',
                  color='conversion_flag',
                  color_continuous_scale=['#F5DEB3', '#D2691E', '#8B4513'])
fig_bar2.update_layout(paper_bgcolor='#F5F0E8',
                       plot_bgcolor='#F5F0E8',
                       xaxis_title='Region',
                       yaxis_title='Conversion Rate')
fig_bar2.write_html("bar_region_conversion.html")
print("  [SAVED] bar_region_conversion.html")

ai_counts = df['ai_assistant_used'].value_counts().reset_index()
ai_counts.columns = ['AI Assistant Used', 'Count']
ai_counts['AI Assistant Used'] = ai_counts['AI Assistant Used'].map({True: 'Yes', False: 'No'})

fig_pie1 = px.pie(ai_counts, values='Count', names='AI Assistant Used',
                  title='<b>AI Assistant Usage Distribution</b>',
                  color_discrete_sequence=['#8B4513', '#D2691E'])
fig_pie1.update_layout(paper_bgcolor='#F5F0E8',
                       plot_bgcolor='#F5F0E8')
fig_pie1.write_html("pie_ai_usage.html")
print("  [SAVED] pie_ai_usage.html")

# ============================================
# SECTION 8: TIME SERIES ANALYSIS
# ============================================
print("\n" + "=" * 70)
print("SECTION 8: TIME SERIES ANALYSIS")
print("=" * 70)

df['timestamp'] = pd.to_datetime(df['timestamp'])
daily_trends = df.groupby(df['timestamp'].dt.date).agg({
    'lead_score': 'mean',
    'satisfaction_score': 'mean',
    'conversion_flag': 'mean'
}).reset_index()
daily_trends.columns = ['date', 'avg_lead_score', 'avg_satisfaction', 'conversion_rate']

fig_line1 = px.line(daily_trends, x='date', y=['avg_lead_score', 'avg_satisfaction'],
                    title='<b>Daily Trends: Lead Score & Satisfaction</b>',
                    color_discrete_sequence=['#8B4513', '#D2691E'])
fig_line1.update_layout(paper_bgcolor='#F5F0E8',
                        plot_bgcolor='#F5F0E8',
                        xaxis_title='Date',
                        yaxis_title='Score')
fig_line1.write_html("timeseries_daily_scores.html")
print("  [SAVED] timeseries_daily_scores.html")

# ============================================
# SECTION 9: SUMMARY REPORT
# ============================================
print("\n" + "=" * 70)
print("SECTION 9: EXECUTIVE SUMMARY REPORT")
print("=" * 70)

summary_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Statistical Analysis Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #F5F0E8; color: #4A2F1A; }}
        h1 {{ color: #8B4513; border-bottom: 2px solid #8B4513; padding-bottom: 10px; }}
        h2 {{ color: #D2691E; margin-top: 30px; }}
        .summary-box {{ background-color: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }}
        .stat {{ font-size: 24px; font-weight: bold; color: #8B4513; }}
        .insight {{ background-color: #E8DCCA; padding: 15px; border-left: 4px solid #8B4513; margin: 15px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background-color: #8B4513; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 8px; border-bottom: 1px solid #DDD; }}
        .chart-link {{ display: inline-block; background-color: #8B4513; color: white; padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 5px; }}
        .chart-link:hover {{ background-color: #D2691E; }}
    </style>
</head>
<body>
    <h1>AI-Solutions Statistical Analysis Report</h1>
    <p><strong>Analysis Date:</strong> {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Records Analyzed:</strong> {len(df):,}</p>
    
    <div class="summary-box">
        <h2>Key Statistics Summary</h2>
        <table>
            <tr><th>Metric</th><th>Value</th><th>Insight</th></tr>
            <tr><td>Average Lead Score</td><td class="stat">{df['lead_score'].mean():.1f}</td><td>Out of 100</td></tr>
            <tr><td>Average Satisfaction</td><td class="stat">{df['satisfaction_score'].mean():.2f}/5</td><td>{'Good' if df['satisfaction_score'].mean() > 3.5 else 'Needs Improvement'}</td></tr>
            <tr><td>Conversion Rate</td><td class="stat">{df['conversion_flag'].mean()*100:.1f}%</td><td>Percentage of visitors who converted</td></tr>
            <tr><td>AI Assistant Usage</td><td class="stat">{df['ai_assistant_used'].mean()*100:.1f}%</td><td>Percentage using AI assistant</td></tr>
            <tr><td>Avg Response Time</td><td class="stat">{df['response_time_ms'].mean():.0f} ms</td><td>{'Good' if df['response_time_ms'].mean() < 1000 else 'Slow'}</td></tr>
        </table>
    </div>
    
    <div class="insight">
        <h3>Key Insights</h3>
        <ul>
            <li><strong>Lead Score Distribution:</strong> The mean lead score is {df['lead_score'].mean():.1f} with a standard deviation of {df['lead_score'].std():.1f}.</li>
            <li><strong>Satisfaction Correlation:</strong> {'Positive' if corr_matrix.loc['lead_score', 'satisfaction_score'] > 0 else 'Negative'} correlation ({corr_matrix.loc['lead_score', 'satisfaction_score']:.3f}) between lead score and satisfaction.</li>
            <li><strong>Response Time Impact:</strong> Correlation of {corr_matrix.loc['response_time_ms', 'satisfaction_score']:.3f} with satisfaction.</li>
            <li><strong>Conversion Performance:</strong> Best performing region: {region_conv.iloc[0]['region']} with {region_conv.iloc[0]['conversion_flag']*100:.1f}% conversion rate.</li>
            <li><strong>Top Country:</strong> {country_lead.iloc[0]['country']} has the highest average lead score at {country_lead.iloc[0]['lead_score']:.1f}.</li>
        </ul>
    </div>
    
    <div class="summary-box">
        <h2>Generated Charts & Visualizations</h2>
        <p>Click any link below to view the interactive visualization:</p>
        <div>
            <a href="table_1_central_tendency.html" class="chart-link" target="_blank">Central Tendency Table</a>
            <a href="table_2_dispersion.html" class="chart-link" target="_blank">Dispersion Table</a>
            <a href="boxplots_combined.html" class="chart-link" target="_blank">Box Plots (Combined)</a>
            <a href="correlation_matrix.html" class="chart-link" target="_blank">Correlation Matrix</a>
            <a href="histogram_lead_score.html" class="chart-link" target="_blank">Lead Score Histogram</a>
            <a href="histogram_satisfaction.html" class="chart-link" target="_blank">Satisfaction Histogram</a>
            <a href="histogram_response_time.html" class="chart-link" target="_blank">Response Time Histogram</a>
            <a href="scatter_response_lead.html" class="chart-link" target="_blank">Response vs Lead Scatter</a>
            <a href="scatter_lead_satisfaction.html" class="chart-link" target="_blank">Lead vs Satisfaction Scatter</a>
            <a href="bar_country_lead.html" class="chart-link" target="_blank">Lead Score by Country</a>
            <a href="bar_region_conversion.html" class="chart-link" target="_blank">Conversion by Region</a>
            <a href="pie_ai_usage.html" class="chart-link" target="_blank">AI Usage Pie Chart</a>
            <a href="timeseries_daily_scores.html" class="chart-link" target="_blank">Daily Trends Time Series</a>
        </div>
    </div>
    
    <div class="summary-box">
        <h2>Recommendations</h2>
        <ul>
            <li><strong>Improve Response Time:</strong> Current average response time is {df['response_time_ms'].mean():.0f}ms. Target under 1000ms for better user experience.</li>
            <li><strong>Focus on Top Regions:</strong> Allocate marketing budget to {region_conv.iloc[0]['region']} which shows highest conversion.</li>
            <li><strong>AI Assistant Enhancement:</strong> Current AI usage is {df['ai_assistant_used'].mean()*100:.1f}%. Promote AI features to increase adoption.</li>
        </ul>
    </div>
    
    <p style="text-align: center; margin-top: 50px; color: #8B4513;">
        <strong>AI-Solutions Analytics Dashboard</strong><br>
        Report Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
    </p>
</body>
</html>
"""

with open("statistical_analysis_report.html", "w", encoding="utf-8") as f:
    f.write(summary_html)

print("\n[SAVED] statistical_analysis_report.html")

# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "=" * 70)
print("ANALYSIS COMPLETE!")
print("=" * 70)

print("\nGenerated Files (14 total):")
print("  [TABLE] table_1_central_tendency.html")
print("  [TABLE] table_2_dispersion.html")
print("  [BOXPLOT] boxplot_lead_score.html")
print("  [BOXPLOT] boxplot_satisfaction.html")
print("  [BOXPLOT] boxplot_response_time.html")
print("  [BOXPLOT] boxplots_combined.html")
print("  [HEATMAP] correlation_matrix.html")
print("  [HISTOGRAM] histogram_lead_score.html")
print("  [HISTOGRAM] histogram_satisfaction.html")
print("  [HISTOGRAM] histogram_response_time.html")
print("  [SCATTER] scatter_response_lead.html")
print("  [SCATTER] scatter_lead_satisfaction.html")
print("  [BAR] bar_country_lead.html")
print("  [BAR] bar_region_conversion.html")
print("  [PIE] pie_ai_usage.html")
print("  [LINE] timeseries_daily_scores.html")
print("  [REPORT] statistical_analysis_report.html")

print("\n" + "=" * 70)
print("TO VIEW RESULTS:")
print("1. Open 'statistical_analysis_report.html' in your web browser")
print("2. Click any chart link to view interactive visualizations")
print("3. All charts are interactive - hover, zoom, pan")
print("=" * 70)