#streamlit run smple.py

import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
import networkx as nx
from mlxtend.frequent_patterns import fpgrowth, association_rules
import io

# --- CONFIGURATION AND STYLING ---
st.set_page_config(
    page_title="FP-Growth Web Log Mining Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
/* 🌌 GENERAL APP STYLING */
.stApp {
    background: radial-gradient(circle at top left, #17172b 0%, #0e0e1a 100%);
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: #e5e5f7;
}
header, footer {visibility: hidden;}
a {color: #9a9aff !important; text-decoration: none;}
a:hover {text-decoration: underline;}

/* 🌈 HEADER */
.header-container {
    text-align: center;
    padding: 40px 25px 30px 25px;
    border-radius: 18px;
    margin-bottom: 50px;
    background: linear-gradient(145deg, #202046, #1b1b35);
    border: 1px solid rgba(90,90,250,0.25);
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
    transition: all 0.4s ease;
}
.header-container:hover {transform: translateY(-2px);}
.header-container h1 {
    font-size: 3em;
    font-weight: 900;
    letter-spacing: 0.6px;
    background: linear-gradient(to right, #5b5bfa, #f7559e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
}
.header-container p {
    color: #b0b0d0;
    font-size: 1.15em;
    letter-spacing: 0.3px;
}

/* 🎛️ PANELS */
.css-1r6slb0, .stContainer {
    background: linear-gradient(160deg, #1e1e3f 0%, #2a2a58 100%);
    border-radius: 20px;
    padding: 28px !important;
    border: 1px solid rgba(255,255,255,0.07);
    box-shadow: 0 6px 25px rgba(0,0,0,0.4);
    transition: all 0.35s ease-in-out;
}
.css-1r6slb0:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(91,91,250,0.3);
}

/* 🧭 PANEL HEADERS */
.panel-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 25px;
}
.panel-icon {
    font-size: 1.9em;
    background: linear-gradient(135deg, #5b5bfa, #f7559e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
h2 {
    font-weight: 700;
    font-size: 1.5em;
    letter-spacing: 0.4px;
    margin-bottom: 0;
    color: #e5e5f7;
}

/* 🎨 BUTTONS */
.stButton > button {
    border: none !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, #5b5bfa, #f7559e) !important;
    color: #fff !important;
    font-weight: 600 !important;
    transition: all 0.25s ease;
}
.stButton > button:hover {
    box-shadow: 0 0 18px rgba(247,85,158,0.4);
    transform: translateY(-2px);
}
.stButton > button:disabled {
    opacity: 0.5 !important;
    cursor: not-allowed !important;
}

/* 🎚️ SLIDERS */
div[data-testid="stSlider"] label {
    color: #b8b8d6 !important;
    font-weight: 600 !important;
}
div[data-testid="stSlider"] div[role="slider"] {
    background: linear-gradient(135deg, #5b5bfa, #f7559e) !important;
}

/* 📊 DATAFRAMES */
.stDataFrame table {
    border-radius: 10px;
    border-collapse: collapse;
}
.stDataFrame thead th {
    background: #28285a !important;
    color: #e5e5ff !important;
    font-weight: 700 !important;
}
.stDataFrame tbody td {
    background: #23234b !important;
    color: #e0e0f0 !important;
    font-size: 0.9em;
}

/* 💡 METRIC CARDS */
.metric-card {
    border-radius: 14px;
    padding: 18px;
    background: linear-gradient(145deg, #25254a, #2d2d60);
    border: 1px solid rgba(255,255,255,0.05);
    text-align: center;
    transition: all 0.3s ease;
}
.metric-card:hover {transform: scale(1.02);}
.metric-value {
    font-size: 1.9em;
    font-weight: 800;
    background: linear-gradient(135deg, #5b5bfa, #f7559e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-label {
    font-size: 0.9em;
    color: #b8b8d6;
}

/* 🧾 FILE UPLOADER */
.stFileUploader {
    border: 2px dashed rgba(91,91,250,0.7) !important;
    background: rgba(91,91,250,0.08) !important;
    border-radius: 14px !important;
    padding: 20px !important;
    text-align: center;
}

/* ✨ EXPANDERS */
.streamlit-expanderHeader {
    font-weight: 600 !important;
    color: #f0f0f0 !important;
}

/* 🧩 SECTION DIVIDER */
.section-divider {
    height: 3px;
    margin: 40px 0;
    background: linear-gradient(to right, #5b5bfa, #f7559e);
    border-radius: 3px;
    opacity: 0.7;
    animation: glow 4s infinite alternate;
}
@keyframes glow {
    from {opacity: 0.4;}
    to {opacity: 1;}
}

/* 📦 DOWNLOAD BUTTON */
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #5b5bfa, #f7559e) !important;
    color: #fff !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    box-shadow: 0 0 15px rgba(247,85,158,0.3);
}

/* ⚠️ ALERT MESSAGES */
.stSuccess, .stWarning, .stError, .stInfo {
    border-radius: 10px !important;
    font-size: 0.9em !important;
}
.stSuccess {background: rgba(50,205,50,0.15) !important;}
.stWarning {background: rgba(247,85,158,0.15) !important;}
.stError {background: rgba(229,62,62,0.15) !important;}
.stInfo {background: rgba(91,91,250,0.12) !important;}
/* --- Dropdown Position Fix --- */
div[data-baseweb="select"] {
    position: relative !important;
}

/* Force dropdown menu to appear under the box */
ul[role="listbox"] {
    position: absolute !important;
    top: 100% !important;
    margin-top: 8px !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 9999 !important;
    background: #1e1e3f !important;
    border: 1px solid #353556 !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5) !important;
    animation: dropdownFadeIn 0.25s ease-in-out;
    overflow: hidden;
}

/* Dropdown items styling */
ul[role="listbox"] li {
    color: #e0e0e0 !important;
    padding: 10px 16px !important;
    transition: all 0.2s ease !important;
}

ul[role="listbox"] li:hover {
    background: linear-gradient(135deg, #5b5bfa33, #f7559e33) !important;
    color: #ffffff !important;
}

/* Smooth fade-in animation */
@keyframes dropdownFadeIn {
    from { opacity: 0; transform: translateY(-5px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>

""", unsafe_allow_html=True)


# --- INITIALIZE SESSION STATE ---
if 'df' not in st.session_state:
    st.session_state.df = None
if 'rules' not in st.session_state:
    st.session_state.rules = None
if 'frequent_itemsets' not in st.session_state:
    st.session_state.frequent_itemsets = None
if 'filtered_pages' not in st.session_state:
    st.session_state.filtered_pages = None

# --- ML MODEL FUNCTIONS ---
def extract_page(url):
    """Extract page name from URL"""
    match = re.search(r'/([\w\-]+)', str(url))
    return match.group(1) if match else None

def preprocess_data(df):
    """Preprocess the web log data"""
    df.columns = [c.strip() for c in df.columns]
    
    # Filter successful requests
    if 'Status' in df.columns:
        df = df[df['Status'].astype(str).str.isdigit()]
        df['Status'] = df['Status'].astype(int)
        df = df[df['Status'] == 200]
    
    # Extract pages from URLs
    df['Page'] = df['URL'].apply(extract_page)
    df = df[df['Page'].notna()]
    
    return df

def create_sessions(df):
    """Create realistic sessions from the data"""
    sessions = []
    for ip, group in df.groupby('IP'):
        pages = list(group['Page'])
        # Break into sub-sessions of size up to 10 pages
        for i in range(0, len(pages), 10):
            sub_session = list(set(pages[i:i+10]))
            if len(sub_session) > 1:
                sessions.append(sub_session)
    
    return sessions

def run_fp_growth_analysis(df, min_support=0.05, min_confidence=0.4):
    """Run the complete FP-Growth analysis"""
    
    # Create sessions
    sessions = create_sessions(df)
    st.info(f"🧩 Total Sessions Formed: {len(sessions)}")
    
    # Calculate page frequencies and filter
    page_counts = df['Page'].value_counts()
    filtered_pages = page_counts[(page_counts > 3) & (page_counts < 400)].index.tolist()
    
    # One-hot encoding
    encoded_data = []
    for session in sessions:
        row = {page: (page in session) for page in filtered_pages}
        encoded_data.append(row)
    encoded_df = pd.DataFrame(encoded_data).fillna(False)
    
    # FP-Growth Mining
    with st.spinner("⏳ Mining Frequent Itemsets..."):
        frequent_itemsets = fpgrowth(encoded_df, min_support=min_support, 
                                   use_colnames=True, max_len=3)
        frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False)
    
    st.success(f"✅ Frequent Itemsets Found: {len(frequent_itemsets)}")
    
    # Association Rules
    if len(frequent_itemsets) > 0:
        rules = association_rules(frequent_itemsets, metric="confidence", 
                                min_threshold=min_confidence)
        rules = rules[(rules['lift'] > 1) & (rules['confidence'] < 1)]
        rules = rules.sort_values(by=['confidence', 'lift'], ascending=False)
    else:
        rules = pd.DataFrame()
    
    # Store in session state
    st.session_state.frequent_itemsets = frequent_itemsets
    st.session_state.rules = rules
    st.session_state.filtered_pages = filtered_pages
    st.session_state.encoded_df = encoded_df
    
    return frequent_itemsets, rules, filtered_pages

def create_visualizations(rules):
    """Create visualizations for the rules"""
    if rules is None or len(rules) == 0:
        return None, None
    
    top_rules = rules.head(10)
    
    # Bar Chart
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    rule_labels = [f"{list(a)[0]} → {list(c)[0]}" for a, c in 
                   zip(top_rules['antecedents'], top_rules['consequents'])]
    
    bars = ax1.barh(rule_labels, top_rules['confidence'], color='skyblue')
    ax1.set_xlabel("Confidence")
    ax1.set_title("Top 10 Association Rules (by Confidence)")
    ax1.invert_yaxis()
    
    # Add value labels on bars
    for bar, conf in zip(bars, top_rules['confidence']):
        width = bar.get_width()
        ax1.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
                f'{conf:.2f}', ha='left', va='center')
    
    plt.tight_layout()
    
    # Network Graph
    fig2, ax2 = plt.subplots(figsize=(12, 8))
    G = nx.DiGraph()
    
    for _, row in top_rules.iterrows():
        for a in row['antecedents']:
            for c in row['consequents']:
                G.add_edge(a, c, weight=row['confidence'])
    
    pos = nx.spring_layout(G, k=0.7, seed=42)
    edges = G.edges(data=True)
    weights = [G[u][v]['weight'] * 3 for u, v, _ in edges]
    
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=1500, alpha=0.7, ax=ax2)
    nx.draw_networkx_edges(G, pos, width=weights, alpha=0.6, 
                          edge_color='gray', arrows=True, ax=ax2)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold', ax=ax2)
    
    ax2.set_title("Association Rule Network")
    ax2.axis('off')
    plt.tight_layout()
    
    return fig1, fig2

def recommend_next_page(current_page, rules, top_n=3):
    """Generate recommendations based on current page"""
    if rules is None or len(rules) == 0:
        return [("⚠️ No strong recommendations found", 0)]
    
    related_rules = rules[rules['antecedents'].apply(lambda x: current_page in x)]
    if related_rules.empty:
        return [("⚠️ No strong recommendations found", 0)]
    
    related_rules = related_rules[['consequents','confidence']].head(top_n)
    recs = []
    for _, row in related_rules.iterrows():
        for p in row['consequents']:
            recs.append((p, row['confidence']))
    
    # Remove duplicates and sort by confidence
    recs = sorted(set(recs), key=lambda x: x[1], reverse=True)
    return recs[:top_n]

# --- STREAMLIT UI COMPONENTS ---
def render_header():
    """Render the dashboard header"""
    st.markdown("""
    <div class="header-container">
        <h1>FP-Growth Web Log Mining Dashboard</h1>
        <p>Discover association rules and patterns in web navigation data</p>
    </div>
    """, unsafe_allow_html=True)

def render_dataset_panel():
    """Render the dataset upload and management panel"""
    st.markdown("<h2>📁 Dataset Panel</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Web Log CSV File", 
            type=["csv"], 
            help="Upload your web log CSV file with columns like IP, URL, Status"
        )
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = preprocess_data(df)
                st.success(f"✅ Data loaded successfully! {len(st.session_state.df)} records")
            except Exception as e:
                st.error(f"❌ Error loading file: {e}")
    
    with col2:
        if st.button("📊 Show Data Summary", use_container_width=True):
            if st.session_state.df is not None:
                st.write("**Data Summary:**")
                st.write(f"- Total records: {len(st.session_state.df)}")
                st.write(f"- Unique IPs: {st.session_state.df['IP'].nunique()}")
                st.write(f"- Unique Pages: {st.session_state.df['Page'].nunique()}")
                st.write(f"- Date range: {st.session_state.df.get('Timestamp', 'N/A')}")
            else:
                st.warning("Please upload data first")
    
    # Display data preview
    if st.session_state.df is not None:
        with st.expander("📋 Data Preview"):
            st.dataframe(st.session_state.df.head(10), use_container_width=True)

def render_mining_panel():
    """Render the mining configuration panel"""
    st.markdown("<h2>⚙️ Mining Panel</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        min_support = st.slider(
            "Minimum Support:",
            min_value=0.01, max_value=0.30, value=0.05, step=0.01, 
            format="%.2f", 
            help="Minimum frequency of itemset occurrence"
        )
        st.markdown(f"<div class='slider-labels'><span>1%</span><span>30%</span></div>", unsafe_allow_html=True)
    
    with col2:
        min_confidence = st.slider(
            "Minimum Confidence:",
            min_value=0.10, max_value=0.90, value=0.40, step=0.05,
            format="%.2f",
            help="Minimum confidence for association rules"
        )
        st.markdown(f"<div class='slider-labels'><span>10%</span><span>90%</span></div>", unsafe_allow_html=True)
    
    if st.button("🚀 Run FP-Growth Analysis", use_container_width=True, 
                disabled=st.session_state.df is None):
        if st.session_state.df is not None:
            with st.spinner("Running FP-Growth analysis..."):
                frequent_itemsets, rules, filtered_pages = run_fp_growth_analysis(
                    st.session_state.df, min_support, min_confidence
                )
            
            if len(rules) > 0:
                st.success(f"✅ Analysis complete! Generated {len(rules)} rules")
            else:
                st.warning("⚠️ No rules generated. Try adjusting parameters.")
        else:
            st.warning("Please upload data first")

def render_visualization_panel():
    """Render the visualization panel"""
    st.markdown("<h2>📊 Visualization Panel</h2>", unsafe_allow_html=True)
    
    if st.session_state.rules is not None and len(st.session_state.rules) > 0:
        fig1, fig2 = create_visualizations(st.session_state.rules)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.pyplot(fig1)
        
        with col2:
            st.pyplot(fig2)
    else:
        st.info("Run the FP-Growth analysis to see visualizations")

def render_recommendation_panel():
    """Render the recommendation panel"""
    st.markdown("<h2>💡 Recommendation Panel</h2>", unsafe_allow_html=True)
    
    if st.session_state.df is not None and st.session_state.filtered_pages is not None:
        page_options = ['Select a page...'] + st.session_state.filtered_pages
        
        selected_page = st.selectbox(
            "Choose a current page:",
            options=page_options,
            index=0
        )
        
        if selected_page != 'Select a page...':
            if st.button("Get Recommendations", use_container_width=True):
                recommendations = recommend_next_page(
                    selected_page, st.session_state.rules
                )
                
                st.write(f"**Recommendations for '{selected_page}':**")
                for i, (rec_page, confidence) in enumerate(recommendations, 1):
                    st.write(f"{i}. **{rec_page}** (confidence: {confidence:.1%})")
    else:
        st.info("Upload data and run analysis to get recommendations")

def render_rules_panel():
    """Render the association rules display panel"""
    st.markdown("<h2>📋 Association Rules</h2>", unsafe_allow_html=True)
    
    if st.session_state.rules is not None and len(st.session_state.rules) > 0:
        # Display rules summary
        st.write(f"**Total Rules Generated:** {len(st.session_state.rules)}")
        
        # Show top rules
        display_rules = st.session_state.rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(20)
        
        # Format antecedents and consequents for better display
        display_rules['Rule'] = display_rules.apply(
            lambda x: f"{set(x['antecedents'])} → {set(x['consequents'])}", axis=1
        )
        display_rules = display_rules[['Rule', 'support', 'confidence', 'lift']]
        
        st.dataframe(display_rules, use_container_width=True)
        
        # Export option
        csv = st.session_state.rules[['antecedents','consequents','support','confidence','lift']].to_csv(index=False)
        st.download_button(
            label="📥 Export Rules as CSV",
            data=csv,
            file_name='association_rules.csv',
            mime='text/csv',
            use_container_width=True
        )
    else:
        st.info("No rules available. Run the FP-Growth analysis to generate rules.")

# --- MAIN DASHBOARD LAYOUT ---
def main():
    render_header()
    
    # Main dashboard grid
    col1, col2 = st.columns(2)
    
    with col1:
        render_dataset_panel()
    
    with col2:
        render_mining_panel()
    
    # Visualization panel (full width)
    render_visualization_panel()
    
    # Bottom panels
    col3, col4 = st.columns(2)
    
    with col3:
        render_recommendation_panel()
    
    with col4:
        render_rules_panel()

if __name__ == "__main__":
    main()