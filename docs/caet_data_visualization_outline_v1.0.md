CAET: Claims Auditing Enhancement Tool
Methodology

Dr. Stacy Lisa Toriola, MD, MSc


Abstract

The Claims Auditing Enhancement Tool (CAET) is a fraud risk-scoring
system developed to identify potentially fraudulent durable medical
equipment (DME) claims within Medicare data. Using the Centers for
Medicare & Medicaid Services (CMS) 2023 DME Supplier/Provider dataset,
two hypotheses were tested: general DME fraud detection (H1) and
intermittent catheter fraud detection (H2). Statistical signal
detection combined with a member-call verification amplifier was used
to produce tiered composite risk scores for providers. Results
indicated that statistical signals alone were insufficient to
distinguish legitimate high-volume providers from fraudulent ones, and
that member-call data was required to surface high-risk cases.

Research Question

Can statistical fraud signals, derived from Medicare DME claims data
alone, reliably distinguish legitimate high-volume providers from
fraud rings, or is additional corroborating information required to
achieve a reliable risk classification?

Method

Data Source

Data were drawn from the CMS Medicare DME Supplier/Provider 2023
dataset, comprising 463,784 claim-level records after signal
processing (dme_with_signals.csv).

Design

Two hypotheses were defined and tested independently:

    H1 (General DME Fraud Detection). Composite risk scoring was
    applied to the full population of 59,592 providers, with a 70%
    threshold for classification as high risk.

    H2 (Intermittent Catheter Fraud Detection). Composite risk scoring
    was applied to a candidate pool of 41 providers meeting
    catheter-specific criteria, with a 75% threshold for
    classification as high risk.

    Rationale for H2. General DME scoring multiplies each claim by a
    category risk weight and uses cutoffs pooled across all equipment
    types. Both dampen catheter signals, so catheter fraud can go
    undetected relative to other DME categories. H2 therefore uses
    catheter-specific cutoffs and adds catheter bundling signals.

Procedure

For each hypothesis, provider-level signals were aggregated into a
composite score. Two scoring conditions were tested for H1: (a) 
statistical signals alone, applied to the full 59,592-provider
population, and (b) statistical signals combined with member-call
verification data as a risk amplifier. For H2, composite scores were
generated for the full 41-provider candidate pool using the combined
scoring approach.

Results

H1. When tested against the full provider population using
statistical signals alone (no member calls applied), 0% of providers
scored in the HIGH or CRITICAL risk tiers. This indicated that
member-call data functions as a required amplifier of the composite
score rather than an optional enhancement.

H2. Testing the full 41-provider candidate pool with the combined
scoring approach yielded the following tier distribution: 8 providers
(19.5%) scored HIGH, 24 providers scored MEDIUM, and 9 providers
scored LOW. This result fell below the 75% pass threshold set for the
hypothesis.

Discussion

Together, the H1 and H2 findings confirm that statistical claims
signals alone are not sufficient to reliably classify DME fraud risk.
Member-call verification data materially changes classification
outcomes and should be treated as a necessary component of the
scoring model rather than a supplementary one.

Tools and Technology

Data processing and scoring were conducted in Python (pandas). Data
visualization was produced using Matplotlib and Seaborn for exploratory
charts, with Power BI used for the interactive dashboard.

References

Centers for Medicare & Medicaid Services. (2023). Medicare durable
    medical equipment, devices & supplies by referring provider and
    service [(CMS) 2023 DME Supplier/Provider dataset]. U.S. Department of Health and Human Services.

Published Date: 08/07/2026
