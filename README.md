# Real Estate Analytics Platform

An end-to-end data engineering and analytics platform for multi-city real estate insights using AWS S3, Snowpipe, Snowflake, dbt, Star Schema, SCD Type 2, Semantic Views, and Streamlit.

---

## 📌 Project Overview

The Real Estate Analytics Platform converts periodic real estate CSV files into a structured and business-ready analytical system.

The platform automates the flow of data from AWS S3 into Snowflake using Snowpipe, transforms the raw data using dbt, builds a Star Schema with historical tracking using SCD Type 2, and exposes business-ready data through semantic views and an interactive Streamlit dashboard.

The main objective is to create a repeatable pipeline from raw operational data to trusted analytical information.

### End-to-End Flow

CSV Files → AWS S3 → Snowpipe → Snowflake RAW → dbt → Data Warehouse → Semantic Views → Streamlit

---

## 🎯 Problem Statement

Real estate data is received as separate periodic extracts for cities, developers, properties, and transactions.

Processing these files independently creates several challenges:

- Source data is scattered across multiple files.
- Manual ingestion and transformation can be difficult to operate consistently.
- Historical changes to developer and property attributes may be lost when records are overwritten.
- Raw data is not suitable for direct business analysis.
- Business users need reliable KPIs, trends, filters, and drilldowns.

This project addresses these challenges by implementing an automated ingestion, transformation, historical tracking, and analytics pipeline.

---

## 🎯 Project Objectives

- Automate CSV ingestion into Snowflake using Snowpipe.
- Store raw source data with ingestion audit metadata.
- Build a curated Star Schema for analytical reporting.
- Implement SCD Type 2 for Developer and Property dimensions.
- Preserve historical versions of changing master data.
- Implement incremental processing using dbt.
- Prevent duplicate transaction-line records.
- Handle late-arriving transaction dates.
- Create semantic views for business analytics.
- Provide an interactive Streamlit dashboard.
- Implement ingestion error monitoring and reject auditing.

---

## 🏗️ Architecture

<img width="961" height="608" alt="image" src="https://github.com/user-attachments/assets/f6859bf8-3130-44ca-95ad-a17b2dca4343" />

