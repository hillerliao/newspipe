#! /usr/bin/env python
# -*- coding: utf-8 -*-

# pyAggr3g470r - A Web based news aggregator.
# Copyright (C) 2010-2013  Cédric Bonhomme - http://cedricbonhomme.org/
#
# For more information : http://bitbucket.org/cedricbonhomme/pyaggr3g470r/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 4.2 $"
__date__ = "$Date: 2010/01/29 $"
__revision__ = "$Date: 2013/11/10 $"
__copyright__ = "Copyright (c) Cedric Bonhomme"
__license__ = "GPLv3"


from flask import render_template, request, flash, session, url_for, redirect, g
from wtforms import TextField, PasswordField, SubmitField, validators
from flask.ext.mail import Message, Mail
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user, AnonymousUserMixin

from collections import defaultdict

from forms import SigninForm, AddFeedForm
from pyaggr3g470r import app, db


import feedgetter
import models

mail = Mail()

login_manager = LoginManager()
login_manager.init_app(app)

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        pass
        #g.user.last_seen = datetime.utcnow()
        #db.session.add(g.user)
        #db.session.commit()

@app.errorhandler(403)
def authentication_failed(e):
    flash('Authenticated failed.')
    return redirect(url_for('login'))

@app.errorhandler(401)
def authentication_failed(e):
    flash('Authenticated required.')
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(email):
    # Return an instance of the User model
    return models.User.objects(email=email).first()

@app.route('/login/', methods=['GET', 'POST'])
def login():
    g.user = AnonymousUserMixin()
    form = SigninForm()

    if form.validate_on_submit():
        user = models.User.objects(email=form.email.data).first()
        login_user(user)
        g.user = user
        flash("Logged in successfully.")
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    """
    Remove the user information from the session.
    """
    logout_user()
    return redirect(url_for('home'))





@app.route('/')
@login_required
def home():
    user = g.user
    feeds = models.User.objects(email=g.user.email).fields(slice__feeds__articles=9).first().feeds
    return render_template('home.html', user=user, feeds=feeds)

@app.route('/fetch/', methods=['GET'])
@login_required
def fetch():
    feed_getter = feedgetter.FeedGetter(g.user.email)
    feed_getter.retrieve_feed()
    return redirect(url_for('home'))

@app.route('/about/', methods=['GET'])
@login_required
def about():
    return render_template('about.html')

@app.route('/feeds/', methods=['GET'])
@login_required
def feeds():
    feeds = models.User.objects(email=g.user.email).first().feeds
    return render_template('feeds.html', feeds=feeds)

@app.route('/feed/<feed_id>', methods=['GET'])
@login_required
def feed(feed_id=None):
    user = models.User.objects(email=g.user.email, feeds__oid=feed_id).first()
    for feed in user.feeds:
        if str(feed.oid) == feed_id:
            return render_template('feed.html', feed=feed)

@app.route('/article/<article_id>', methods=['GET'])
@login_required
def article(article_id=None):
    #user = models.User.objects(email=g.user.email, feeds__oid=feed_id).first()
    article = models.Article.objects(id=article_id).first()
    if not article.readed:
        article.readed = True
        article.save()
    return render_template('article.html', article=article)

@app.route('/mark_as_read/', methods=['GET'])
@login_required
def mark_as_read():
    #user = models.User.objects(email=g.user.email).first()
    models.Article.objects(readed=False).update(set__readed=True)
    return redirect(url_for('home'))

@app.route('/delete/<article_id>', methods=['GET'])
@login_required
def delete(article_id=None):
    user = models.User.objects(email=g.user.email).first()
    # delete the article
    for feed in user.feeds:
        for article in feed.articles:
            if str(article.id) == article_id:
                feed.articles.remove(article)
                article.delete()
                user.save()
                return redirect(url_for('home'))

@app.route('/articles/<feed_id>', methods=['GET'])
@login_required
def articles(feed_id=None):
    user = models.User.objects(email=g.user.email, feeds__oid=feed_id).first()
    for feed in user.feeds:
        if str(feed.oid) == feed_id:
            return render_template('articles.html', feed=feed)

@app.route('/favorites/', methods=['GET'])
@login_required
def favorites():
    user = models.User.objects(email=g.user.email).first()
    result = []
    for feed in user.feeds:
        feed.articles = [article for article in feed.articles if article.like]
        if len(feed.articles) != 0:
            result.append(feed)
    return render_template('favorites.html', feeds=result)

@app.route('/unread/', methods=['GET'])
@login_required
def unread():
    user = models.User.objects(email=g.user.email).first()
    result = []
    for feed in user.feeds:
        feed.articles = [article for article in feed.articles if not article.readed]
        if len(feed.articles) != 0:
            result.append(feed)
    return render_template('unread.html', feeds=result)

@app.route('/management/', methods=['GET'])
@login_required
def management():
    form = AddFeedForm()
    user = models.User.objects(email=g.user.email).first()
    nb_feeds = len(user.feeds)
    nb_articles = sum([len(feed.articles) for feed in user.feeds])
    nb_unread_articles = sum([len([article for article in feed.articles if not article.readed]) for feed in user.feeds])
    return render_template('management.html', form=form, \
                            nb_feeds=nb_feeds, nb_articles=nb_articles, nb_unread_articles=nb_unread_articles)

@app.route('/edit_feed/', methods=['GET', 'POST'])
@app.route('/edit_feed/<feed_id>', methods=['GET', 'POST'])
@login_required
def edit_feed(feed_id=None):
    """
    Add or edit a feed.
    """
    user = models.User.objects(email=g.user.email).first()
    form = AddFeedForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('edit_feed.html', form=form)
        if feed_id != None:
            # Edit an existing feed
            for feed in user.feeds:
                if str(feed.oid) == feed_id:
                    form.populate_obj(feed)
                    user.save()
                    flash('Feed "' + feed.title + '" successfully updated', 'success')
                    return redirect('/feed/'+feed_id)
        else:
            # Create a new feed
            new_feed = models.Feed(title=form.title.data, link=form.link.data, \
                                    site_link=form.site_link.data, email=form.email_notification.data)
            user.feeds.append(new_feed)
            user.feeds = sorted(user.feeds, key=lambda t: t.title.lower())
            user.save()
            return redirect(url_for('home'))

    if request.method == 'GET':
        if feed_id != None:
            for feed in user.feeds:
                if str(feed.oid) == feed_id:
                    form = AddFeedForm(obj=feed)
                    return render_template('edit_feed.html', action="Edit the feed", form=form, feed=feed)

        # Return an empty form in order to create a new feed
        return render_template('edit_feed.html', action="Add a feed", form=form)

@app.route('/delete_feed/<feed_id>', methods=['GET'])
@login_required
def delete_feed(feed_id=None):
    user = models.User.objects(email=g.user.email).first()
    # delete all articles (Document objects)
    for feed in user.feeds:
        if str(feed.oid) == feed_id:
            for article in feed.articles:
                article.delete()
            feed.articles = []
            # delete the feed (EmbeddedDocument object)
            user.feeds.remove(feed)
            user.save()
            return redirect(url_for('home'))