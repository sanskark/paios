from llm.unified import process_input


def fix_output(user_input, context, bad_result, issues):
    print("Fixing output:", issues)

    fix_prompt = f"""
    The previous output had issues:
    
    {issues}
    
    Original output:
    {bad_result}
    
    Fix the response to:
    - improve answer quality
    - remove invalid values
    - follow rules strictly
    
    Return corrected JSON only.
    """

    fixed = process_input(user_input + "\n" + fix_prompt, context)
    return fixed
