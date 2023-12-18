prompt_li_function = [
  {
    "name": "json_answer",
    "description": "this function arranges the different paragraphs into a json format for later use",
    "parameters": {
      "type": "object",
      "properties": {
        "viability_summary": {
          "type": "string",
          "description": "a 2-3 sentence summary of the candidate's viability for the job description"
        },
        "requirements_table": {
          "type": "object",
          "properties": {
            "Education":{ # REQUIRED EDUCATION
              "type": "object",
              "properties": {
                "measurable": {
                  "type": "boolean",
                  "description": "Mark this as true.",
                },
                "score": {
                  "type": "number",
                  "description": "Score given to required education category, give full points for an exact match, and no points for no match.",
                },
                "explanation": {
                  "type": "string",
                  "description": "Explanation for the score given.",
                }
              },
              "required": ["required", "score", "explanation"]
            },
            "Experience": { # REQUIRED EXPERIENCE
              "type": "object",
              "properties": {
                "measurable": {
                  "type": "boolean",
                  "description": "Mark this as true.",
                },
                "score": {
                  "type": "number",
                  "description": "Score given to required experience category, give full points for an exact match, and no points for no match.",
                },
                "explanation": {
                  "type": "string",
                  "description": "Explanation for the score given.",
                }
              },
              "required": ["required", "score", "explanation"]
            },
            "Certifications / Licenses": { # REQUIRED CERTIFICATIONS OR LICENSES
              "type": "object",
              "properties": {
                "measurable": {
                  "type": "boolean",
                  "description": "Mark this as true.",
                },
                "score": {
                  "type": "number",
                  "description": "Score given to required certifications / licenses category, give full points for an exact match, and no points for no match.",
                },
                "explanation": {
                  "type": "string",
                  "description": "Explanation for the score given.",
                }
              },
              "required": ["required", "score", "explanation"]
            }
          },
          "required": ["education"]
        },
        "desired_elements_table": {
          "type": "object",
          "properties": {
            "Education":{ # PREFERRED EDUCATION
              "type": "object",
              "properties": {
                "measurable": {
                  "type": "boolean",
                  "description": "Mark this as true.",
                },
                "score": {
                  "type": "number",
                  "description": "Score given to preferred education category, give full points for an exact match, give 1/2 points for close match, and no points for no match.",
                },
                "explanation": {
                  "type": "string",
                  "description": "Explanation for the score given.",
                }
              },
              "required": ["score", "explanation"]
            },
            "Experience": { # PREFERRED EXPERIENCE
              "type": "object",
              "properties": {
                "measurable": {
                  "type": "boolean",
                  "description": "Mark this as true.",
                },
                "score": {
                  "type": "number",
                  "description": "Score given to preferred experience category, give full points for an exact match, give 1/2 points for close match, and no points for no match.",
                },
                "explanation": {
                  "type": "string",
                  "description": "Explanation for the score given.",
                }
              },
              "required": ["required", "score", "explanation"]
            },
            "Certifications / Licenses": { # PREFERRED CERT OR LICENSES
              "type": "object",
              "properties": {
                "measurable": {
                  "type": "boolean",
                  "description": "Mark this as true.",
                },
                "score": {
                  "type": "number",
                  "description": "Score given to preferred certifications / licenses category, give full points for an exact match, give 1/2 points for close match, and no points for no match.",
                },
                "explanation": {
                  "type": "string",
                  "description": "Explanation for the score given.",
                }
              },
              "required": ["required", "score", "explanation"]
            }
          },
          "required": ["education"]
        }
      },
      "required": ["viability_summary","requirements_table","desired_elements_table"]
    }
  }
]