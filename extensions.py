from flask import Flask, Blueprint, render_template, session, redirect, url_for, request, flash

def in_session():
    try:
        email = request.form['email']
        # password = request.form['password']
        existing_user = email
        if existing_user:
            session['email'] = existing_user
            return True
        else:
            return False
    except Exception as e:
        print(f'there was an error: {e}')
        flash(f'there was an error: {e}')
    
def signup_procedure(new_user):
    email = request.form['email']
    # password = request.form['password']
    new_user = email
    return new_user
