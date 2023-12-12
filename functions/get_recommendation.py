def get_recommendation(overall_score):
    if overall_score >= 9:
        return 'Candidate is a great fit.'
    elif overall_score >= 6:
        return 'Candidate is a good fit.'
    else:
        return 'Candidate is not a good fit.'