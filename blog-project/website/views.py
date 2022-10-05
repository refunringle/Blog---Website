from flask import Blueprint, render_template, request,Response, flash, redirect, url_for,jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import db,User,Post,Comment,Category,Like,Image
from slugify import slugify


views = Blueprint("views", __name__)


#Home route

@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    category = Category.query.all()
    return render_template("home.html",current_user=current_user, posts=posts,category=category)




# Post creation route

@views.route("/post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        cat = request.form.get('Category')
        title = request.form.get('title')
        content = request.form.get('content')
        slug=slugify(title)
        if not cat :
            flash('category cannot be empty', category='error')
        elif not title:
            flash('title cannot be empty', category='error') 
        elif not content:
            flash('content cannot be empty', category='error')
        else:
            category = Category.query.filter_by(category = cat).first()
            if category:
                post = Post(title =title,category = category ,content=content, 
                            category_id=category.id,user_id=current_user.id,slug=slug)
            else:
                category = Category(category = cat,cat_user =current_user.id )
                db.session.add(category)
                db.session.commit()
                post = Post(title =title,category = category, content=content, 
                user_id=current_user.id,slug=slug)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))
    category = Category.query.all()
    return render_template('posts.html', categories = category)



# Post view route with slug url of title

@views.route("/post/<int:id>/<slug>", methods=['GET', 'POST'])
def view_post(id,slug):
    slug_= slugify(slug,allow_unicode=True)
    if not slug:
        return redirect(url_for('views.views_post'))
    else:
        post_view = Post.query.filter_by(id=id).all()
        post = db.session.query(Post).filter_by(slug = slug).first()
        comments_ = Comment.query.filter_by(post_id=id).order_by(Comment.timestamp.desc()).all()
    return render_template("view_post.html",current_user=current_user,slug=slug_,
                               post_view=post_view,mycomment=comments_,post=post)
    

# post view without slug url 

@views.route("/post/<int:id>/", methods=['GET', 'POST'])
def views_post_by_id(id):
    post = Post.query.get(id)
    return redirect(url_for("views.view_post",id =post.id, slug =post.slug))



# post deletion route

@views.route("/delete/<int:id>/ ")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    id = current_user.id
    if id == post.user_id:
        db.session.delete(post)
        db.session.commit()
        flash("post deleted",category='success')
        return redirect (url_for('views.user_dashboard',id = id,username=current_user.username))



#comments 

@views.route("/comment/<int:id>/<slug>", methods=['GET','POST'])
def comments(id,slug):
    post_view = Post.query.filter_by(id=id).all()
    slug_= slugify(slug,allow_unicode=True)
    if request.method == "POST":
        guestname = request.form.get('name')
        comment = request.form.get('comment')
        if current_user.is_authenticated:
            if not comment:
                flash('comment section cannot be empty', category='error')
                return redirect(url_for('views.view_post',id=id,slug=slug_))
        else:
            if not guestname :
                flash('name section cannot be empty', category='error')
                return redirect(url_for('views.view_post',id=id,slug=slug_))
            if not comment:
                flash('comment section cannot be empty', category='error')
                return redirect(url_for('views.view_post',id=id,slug=slug_))
            
        if current_user.is_authenticated:
            post = Comment(guestname =current_user.username,user_id=current_user.id,
                           Comment=comment, post_id=id)                
        else:
            post = Comment(guestname =guestname, Comment=comment, post_id=id)
        db.session.add(post)
        db.session.commit()
        flash(f'{post.guestname} commented!', category='success')
        return redirect(url_for('views.view_post',id=id,slug=slug_))
        
    return render_template('view_post.html',post_view=post_view)


# creating category

@views.route("/category", methods=['GET','POST'])
@login_required
def add_category():
    if request.method == "POST":
        cat = request.form.get('category')
        if cat == "":
            flash('category items cannot be empty', category='error')
        else:
            category_exist = Category.query.filter_by(category = cat).first()
            if category_exist:
                flash("category added..")
                return redirect(url_for('views.user_dashboard',id = current_user.id,username=current_user.username))
        category = Category(category = cat,cat_user =current_user.id)
        db.session.add(category)    
        db.session.commit()
        flash("category added..")
        return redirect(url_for('views.user_dashboard',id = current_user.id,username=current_user.username))
    return render_template('posts.html')

    


#category deletion 

@views.route("/category_del/<int:id>/", methods=['GET','POST'])
@login_required
def del_category(id):
    cat =  Category.query.filter_by(id=id).first()
    if request.method == "POST":
        if not cat :
            flash('Input items cannot be empty', category='error')
        else:
            if current_user.id == cat.cat_user:
                db.session.delete(cat)
                db.session.commit()
                flash("category deleted...")
            else:
                flash('not worked', category='error')
            return redirect(url_for('views.user_dashboard', id = current_user.id,username=current_user.username))
    return render_template('home.html')



#category sorting in home page 

@views.route("<int:id>/<category>")
def category_post(id,category):
    posts = Post.query.filter_by(category_id  = id).order_by((Post.timestamp.desc())).all()
    category = Category.query.all()
    return render_template("home.html",current_user=current_user, posts=posts,category=category)




#Likes implementation 

@views.route("/likepost/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
     
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    
    return jsonify({"likes": len(post.likes),
    "liked": current_user.id in map(lambda x: x.user_id, post.likes)})


#user dashboard 

@views.route("/users/<int:id>/<username>")
@login_required
def user_dashboard(id,username):
    img_view = Image.query.filter_by(user_id=id).first() 
    user = User.query.filter_by(id = id).first()
    posts = Post.query.filter_by(user_id = id).order_by((Post.timestamp.desc())).all()
    categories = Category.query.filter_by(cat_user = id).all()
    return render_template("dashboard.html",user = user, categories= categories, posts = posts,img_view =img_view)



# profile picture insertion into database

@views.route("/pic", methods=['POST'])
@login_required
def picture():
    pic = request.files['image']
    if not pic:
        flash('please browse any file', category='error')
        return redirect(url_for('views.user_dashboard',id=current_user.id,username=current_user.username))
    else:
        filename = secure_filename(pic.filename)
        if pic.filename =="":
            flash('No selected file',category='error')
            return redirect(url_for('views.home'))
        else:    
            type=pic.mimetype
            img=Image(img=pic.read(),type=type,img_name=filename ,user_id=current_user.id)
            db.session.add(img)
            db.session.commit()
            flash('Updated successfully')
        return redirect(url_for('views.user_dashboard',id=current_user.id,username=current_user.username))
    


# profile picture view 

@views.route("pic/<int:user_id>", methods=['GET', 'POST'])
def view_img(user_id):
    img_view = Image.query.filter_by(user_id=user_id).order_by((Image.timestamp.desc())).first() 
   
    if not img_view:
        flash ('image not found',category='error')
        return redirect(url_for('views.home'))
    else:
        if img_view.type =="": 
            flash('its not a image',category='error')
        else:
            return Response(img_view.img,mimetype=img_view.type)
    return render_template("dashboard.html",current_user=current_user.id, img_view=img_view)


