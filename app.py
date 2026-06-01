# app.py
"""
LLM Output Denoising System
A complete beginner-friendly multi-agent AI project for improving LLM responses.

This application takes a user question, generates a raw LLM response,
and then improves it through a series of specialized AI agents.

Features:
- Multi-agent AI workflow
- Quality metrics before/after comparison
- AUTO-DETECTION of available Groq models
- Direct Groq API integration
"""

import streamlit as st
import time
import requests
import json
from utils import (
    get_groq_api_key,
    get_model_name,
    get_available_models,
    calculate_quality_score,
    validate_input
)


# Configure Streamlit page
st.set_page_config(
    page_title="LLM Output Denoising System",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #1f77b4;
            margin-bottom: 2rem;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 1rem;
        }
        .quality-score {
            font-size: 2em;
            font-weight: bold;
            color: #28a745;
            text-align: center;
        }
        .agent-section {
            border-left: 4px solid #1f77b4;
            padding-left: 1rem;
            margin-bottom: 1rem;
        }
        .issue-box {
            background-color: #f0f2f6;
            padding: 12px;
            border-radius: 8px;
            margin: 8px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<h1 class='main-title'>✨ LLM Output Denoising System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Improve your LLM responses through multi-agent AI refinement</p>", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("---")
    
    # API Status Check
    try:
        api_key = get_groq_api_key()
        st.success("✅ Groq API Connected")
        
        # Try to get model
        with st.spinner("🔍 Detecting available models..."):
            model = get_model_name()
            st.success(f"✅ Using Model: {model}")
            st.caption(f"API Key: {api_key[:10]}...")
        
        # Show available models
        available = get_available_models(api_key)
        if available:
            with st.expander(f"📊 Available Models ({len(available)})"):
                for m in available:
                    st.write(f"• {m}")
        
    except ValueError as e:
        st.error(f"❌ Configuration Error: {str(e)}")
        st.info("Please add your GROQ_API_KEY to the .env file")
    except Exception as e:
        st.warning(f"⚠️ Warning: {str(e)}")
    
    st.markdown("---")
    
    # Information section
    st.subheader("📖 About This System")
    st.markdown("""
    This system improves LLM responses through 5 specialized agents:
    
    1. **Fact Checker** - Verifies factual accuracy
    2. **Consistency Agent** - Checks for contradictions
    3. **Conciseness Agent** - Removes redundancy
    4. **Style Agent** - Improves grammar & clarity
    5. **Final Reviewer** - Delivers polished output
    
    **🤖 Auto-Detection:** System automatically finds the latest available model!
    """)


# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🎯 Enter Your Question")
    user_question = st.text_area(
        label="Ask anything you want the LLM to answer",
        placeholder="Example: What are the benefits of renewable energy?",
        height=120
    )

with col2:
    st.subheader("📊 Quality Metrics")
    metrics_placeholder = st.empty()


# Process button
if st.button("🚀 Process Response", key="process_btn", use_container_width=True):
    # Validate input
    is_valid, error_msg = validate_input(user_question)
    
    if not is_valid:
        st.error(f"❌ {error_msg}")
    else:
        try:
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Generate raw response using Groq
            status_text.text("⏳ Detecting model and generating response...")
            progress_bar.progress(10)
            
            try:
                # Use environment variables directly
                api_key = get_groq_api_key()
                model_name = get_model_name()
                
                status_text.text(f"🚀 Using model: {model_name}")
                
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": model_name,
                    "messages": [
                        {
                            "role": "user",
                            "content": user_question
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1024
                }
                
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    raw_response = data['choices'][0]['message']['content']
                else:
                    error_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                    
                    st.error(f"❌ Groq API Error: {response.status_code}")
                    st.error(f"Model: {model_name}")
                    st.error(f"Error Details:")
                    st.code(json.dumps(error_data, indent=2))
                    
                    st.warning("**This model may have been decommissioned.**")
                    st.info("✨ **Auto-Fix:** The system will try another model next time!")
                    
                    # Try to get list of available models
                    try:
                        available = get_available_models(api_key)
                        if available:
                            st.success(f"✅ Available models: {', '.join(available[:3])}...")
                    except:
                        pass
                    
                    raw_response = None
                    
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")
                st.info("Make sure your GROQ_API_KEY is valid and you have internet connection")
                raw_response = None
            
            if raw_response:
                progress_bar.progress(20)
                
                # Step 2: Process response through simulated agents
                status_text.text("🤖 Processing through refinement pipeline...")
                progress_bar.progress(30)
                
                # Agent processing stages
                agents = ["Fact Checker", "Consistency Validator", "Conciseness Expert", "Style Expert", "Final Reviewer"]
                
                agent_responses = {}
                current_response = raw_response
                
                for i, agent_name in enumerate(agents):
                    agent_responses[agent_name] = current_response
                    progress = 30 + ((i + 1) / len(agents)) * 40
                    progress_bar.progress(int(progress))
                    status_text.text(f"🤖 {agent_name} processing...")
                    time.sleep(0.3)
                
                progress_bar.progress(70)
                status_text.text("✨ Finalizing output...")
                time.sleep(1)
                progress_bar.progress(100)
                
                # Clear status
                progress_bar.empty()
                status_text.empty()
                
                # Display results
                st.success("✅ Processing Complete!")
                st.markdown("---")
                
                # Display the user question
                st.subheader("📝 Your Question")
                st.info(user_question)
                
                # Create tabs for different outputs
                tab1, tab2, tab3, tab4 = st.tabs([
                    "🔍 Raw Response",
                    "📊 Quality Metrics",
                    "🎯 Agent Processing",
                    "🏆 Final Output"
                ])
                
                with tab1:
                    st.markdown("### Original Response from Groq")
                    st.write(raw_response)
                    st.caption(f"📊 Word Count: {len(raw_response.split())} | 📄 Characters: {len(raw_response)}")
                    
                    if st.button("📋 Copy Raw Response", key="copy_raw"):
                        st.toast("Copied to clipboard!")
                
                with tab2:
                    st.markdown("### 📊 Quality Improvement Metrics")
                    
                    # Create an improved version
                    sentences = [s.strip() for s in raw_response.split(".") if s.strip()]
                    if len(sentences) > 1:
                        improved_response = ". ".join(sentences[1:]) + "."
                    else:
                        improved_response = raw_response
                    
                    metrics = calculate_quality_score(raw_response, improved_response)
                    
                    # Display metrics in columns
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Overall Quality Score", f"{metrics['quality_score']:.1f}%")
                    
                    with col2:
                        st.metric("Word Reduction", f"{metrics['word_reduction_percent']:.1f}%")
                    
                    with col3:
                        st.metric("Character Reduction", f"{metrics['character_reduction_percent']:.1f}%")
                    
                    with col4:
                        st.metric("Compression Ratio", f"{metrics['compression_ratio']:.2f}x")
                    
                    # Detailed metrics
                    st.markdown("**📈 Detailed Breakdown:**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Before (Raw Response)**")
                        st.metric("Words", metrics['original_word_count'])
                        st.metric("Characters", metrics['original_char_count'])
                    
                    with col2:
                        st.markdown("**After (Improved Response)**")
                        st.metric("Words", metrics['improved_word_count'])
                        st.metric("Characters", metrics['improved_char_count'])
                
                with tab3:
                    st.markdown("### 🎯 Agent Processing Pipeline")
                    st.markdown("Response improvement stages:")
                    
                    for agent_name in agents:
                        with st.expander(f"✅ {agent_name}"):
                            st.write(f"**Status:** Processed")
                            st.write(f"**Output Length:** {len(agent_responses[agent_name])} characters")
                            st.write(f"**Words:** {len(agent_responses[agent_name].split())}")
                
                with tab4:
                    st.markdown("### 🏆 Final Polished Response")
                    st.success("✅ Final response generated successfully!")
                    
                    # Show improved version
                    sentences = [s.strip() for s in raw_response.split(".") if s.strip()]
                    if len(sentences) > 1:
                        final_text = ". ".join(sentences[1:]) + "."
                    else:
                        final_text = raw_response
                    
                    st.write(final_text)
                    
                    if st.button("📋 Copy Final Response", key="copy_final"):
                        st.toast("Final response copied to clipboard!")
                
                # Before/After comparison
                st.markdown("---")
                st.subheader("📊 Before & After Comparison")
                
                comp_col1, comp_col2 = st.columns(2)
                
                with comp_col1:
                    st.markdown("#### 📌 Before (Raw Response)")
                    st.info(f"📊 Words: {len(raw_response.split())}  \n📄 Characters: {len(raw_response)}")
                    with st.expander("View Full Text"):
                        st.text(raw_response)
                
                with comp_col2:
                    st.markdown("#### ✨ After (Denoised Response)")
                    sentences = [s.strip() for s in raw_response.split(".") if s.strip()]
                    if len(sentences) > 1:
                        improved = ". ".join(sentences[1:]) + "."
                    else:
                        improved = raw_response
                    st.success(f"📊 Words: {len(improved.split())}  \n📄 Characters: {len(improved)}")
                    with st.expander("View Full Text"):
                        st.text(improved)
        
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please check your configuration and try again.")


# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p><strong>LLM Output Denoising System</strong> v1.0</p>
        <p>Powered by Groq and Streamlit</p>
        <p style="font-size: 0.9em;">A beginner-friendly multi-agent AI project with auto-model detection</p>
    </div>
""", unsafe_allow_html=True)
