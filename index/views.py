from django.shortcuts import render, redirect
from controlpannel.models import Product, Comments, Categories, Product_Side_Images
from authorization.models import User
# Create your views here.
def index(request):
    return render(request,'index.html', {})

def gallery(request):
    obj = Product.objects.all()
    total_categories = Categories.objects.all()

    if request.method == 'POST':
        category = request.POST.get('category')
        if category == 'All':
            obj = Product.objects.all()
        else:
            get_category = Categories.objects.get(category=category)
            obj = Product.objects.filter(P_category = get_category)



    return render(request,'gallery.html', {'product_images':obj, 'category': total_categories})

def product_detail(request,key_id):
    print(key_id)
    product = Product
    product_obj = product.objects.get(P_id=key_id)
    comment = Comments
    obj = comment.objects.filter(P_id=product_obj)
    comment_data = []
    for i in obj:
        comment_data.append({'COMMENT': i.comment, 'NAME': i.user.name})
    side_images = Product_Side_Images.objects.filter(P_id = product_obj)

    if request.method == 'POST':
        message = request.POST.get('message')

        if 'email' in request.session:
            # print(message)
            new_comment = Comments
            check_user = User.objects.get(email=str(request.session['email']))
            get_product = Product.objects.get(P_id=key_id)
            try:
                query = new_comment.objects.get(user=check_user, P_id=key_id)
                print("comment already exists")
                comment = Comments
                obj = comment.objects.filter(P_id=product_obj)
                del comment_data
                comment_data = []
                for i in obj:
                    comment_data.append({'COMMENT': i.comment, 'NAME': i.user.name})

                return render(request, 'product-detail.html', {'P_id':key_id,'data': comment_data, 'image': product_obj,'side_images':side_images, 'error': 'You can enter only one comment' })

            except new_comment.DoesNotExist:
                Comments.objects.create(comment=message, user=check_user, P_id=get_product)
                comment = Comments
                obj = comment.objects.filter(P_id=product_obj)
                del comment_data
                comment_data = []
                for i in obj:
                    comment_data.append({'COMMENT': i.comment, 'NAME': i.user.name})

                return render(request, 'product-detail.html', {'P_id':key_id,'data': comment_data, 'image': product_obj,'side_images':side_images})


        else:
            comment = Comments
            obj = comment.objects.filter(P_id=product_obj)
            del comment_data
            comment_data = []
            for i in obj:
                comment_data.append({'COMMENT': i.comment, 'NAME': i.user.name})
            return render(request, 'product-detail.html', {'P_id':key_id,'data': comment_data, 'image': product_obj,'side_images':side_images, 'error_login':'You need to login first!'})


    #print(comment_data)


    print(product_obj.P_image)

    return  render(request,'product-detail.html', {'P_id':key_id,'data': comment_data, 'image': product_obj,'side_images':side_images,})

def product_side_images(request,key_id):
    product = Product
    product_obj = product.objects.get(P_id=key_id)



    side_images = Product_Side_Images.objects.filter(P_id=product_obj)

    return render(request, 'Product_side_images.html', {'images':side_images})