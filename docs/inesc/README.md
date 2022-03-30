This data repository was created as a supplement to a Systematic Literature Review for Automatic Quality Assessment of Wikipedia Articles we published in (TODO). This repository details the publications we reviewed during the analysis of the state of the art, starting from the Abstract Screening phase. It contains the following files:

screening.csv: Lists the publications that were assessed in the final Screening stage of the Literature Review process, where we assess the paper abstracts. The CSV has the following  structure:

- ID (Assigned paper ID)
- Title
- Year
- URL
- Included (Whether it was included in the following phase)
- Keywords (Separated by commas)
- Authors (Separated by commas)
- Publication Type (Conference or Journal)
- Published In (Publication venue)

eligibility.csv: Lists the publications that were assessed in the Eligibility phase of the Literature Review process, where we read the full text of each paper. For each ID, we indicate whether we included the article in the following phase, and a short explanation for the exclusions. 

inclusion.csv: Lists the relevance scores for all of the included papers. The CSV will contain the IDs and the scores for each question. The four questions and their score ranges can be summarized as:
- Q1. Discussion of Features ([0 − 3])
- Q2. Discussion of ML approaches ([0 − 3])
- Q3. Discussion of Results ([0 − 3])
- Q4. Article Language other than English ([0 − 1])



