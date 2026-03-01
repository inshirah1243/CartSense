# CartSense: Revenue-Aware Add-On Engine

**Submitted by:**   *Inshirah Ibtihaz & Tippana Samhitha*
**Submission for:** Zomathon 2026 – Problem Statement 2  

---

## Overview

This project presents a context-aware recommendation system designed for the Cart Super Add-On (CSAO) rail in a food delivery platform.

The objective is to intelligently recommend complementary add-on items that:

- Maximize expected revenue  
- Improve Average Order Value (AOV)  
- Maintain high acceptance rates  
- Operate under strict real-time latency constraints (200–300ms)

The system balances predictive performance with business impact and production feasibility.

---

## Problem Framing

We model CSAO recommendations as a context-aware ranking problem.

For each cart state, candidate add-on items are ranked using:

**Expected Revenue = P(accept | context) × price × margin**

The system follows a two-stage approach:

1. Predict probability of add-on acceptance  
2. Re-rank candidates based on expected revenue  

This ensures recommendations are both relevant and business-aligned.

---

## Dataset

Since no dataset was provided, we generated a synthetic but realistic dataset simulating:

- Multiple user segments (budget, mid, premium)  
- Mealtime behavior (lunch, dinner, late-night)  
- Weekend vs weekday patterns  
- Varying cart sizes  
- Price sensitivity differences  
- Complementary meal patterns  

The synthetic data was designed to mimic real-world food delivery dynamics.

---

## Feature Engineering

Features were designed across four entities:

### User Features
- User segment  
- Average order value  
- Order frequency  

### Cart Context Features
- Current cart value  
- Cart size  
- Hour bucket  
- Weekend flag  

### Item Features
- Category  
- Price  
- Margin percentage  
- Popularity score  

### Interaction Features
- Category compatibility flag  

The same feature schema is used for training and inference to ensure consistency.

---

## Model Architecture

We use XGBoost as the core prediction engine due to:

- Strong performance on structured behavioral data  
- Ability to capture non-linear interactions  
- Low inference latency  

### Two-Stage Ranking

1. Acceptance probability prediction  
2. Revenue-aware re-ranking  

This improves AOV while preserving recommendation relevance.

---

## Evaluation Results

- **AUC:** ~0.79  
- **Revenue Uplift:** +3.28% compared to probability-only ranking  

These results indicate strong discrimination performance and measurable business improvement.

---

## System Design

### Offline Layer
- Feature aggregation  
- Model training  
- Model storage  

### Online Layer
- Candidate filtering (approximately 50 items)  
- Feature retrieval  
- Probability prediction  
- Revenue-aware ranking  
- Top-N recommendation output  

The system is designed to operate within a **200–300ms latency budget**.

---

## Cold Start Strategy

For new users or sparse histories, the system relies on:

- Popularity score  
- Category compatibility  
- Item margin  

This generates stable recommendations without historical dependency.

---

## A/B Testing Plan

The proposed solution can be evaluated through a controlled A/B experiment comparing:

- Baseline probability-based ranking  
- Revenue-aware ranking system  

Key metrics to track:

- AOV lift  
- Add-on acceptance rate  
- Attach rate  
- Guardrail metrics such as cart abandonment  

---

## Limitations

- The dataset is synthetic and may not fully capture real-world variability  
- Revenue optimization must be balanced with diversity  
- Users with limited history depend more on fallback logic  
- Continuous monitoring and periodic retraining would be required in production  

---

## Conclusion

This project demonstrates how contextual modeling, revenue-aware ranking, and production-conscious system design can improve cart value while maintaining user experience.

The solution balances technical rigor with business alignment, making it suitable for large-scale real-time deployment.
