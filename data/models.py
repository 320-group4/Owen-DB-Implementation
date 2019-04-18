from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Member(models.Model):
    # FK
    visibility = models.BooleanField(default=False, null=True)
    invited_by = models.IntegerField(null=True)

    # ATTRIBUTES 
    email = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=50,null=True)
    username = models.CharField(max_length=50,null=True)
    points = models.IntegerField(null=True)
    user_type = models.CharField(max_length=50,null=True)
    login_time = models.CharField(max_length=50,null=True)
    logout_time = models.CharField(max_length=50,null=True)
    date_create = models.DateTimeField(auto_now_add = True,null=True)
    is_verified = models.BooleanField(default=True,null=True)
    birthday = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.username

    def set_username(self, username):
        self.username = username
 
    def get_username(self):     
        return self.username

    # We are going to make getters and setters for entire attributes in the future


class Post(models.Model):
    post_id = ArrayField(models.IntegerField(null=True), blank=True, null=True)
    comment_id = ArrayField(models.IntegerField(null=True), blank=True, null=True)
    image_id = ArrayField(models.IntegerField(null=True), blank=True, null=True)
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    urls = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now_add=True, null=True)
    is_flagged = models.BooleanField(default=False, null=True)
    content = models.TextField(max_length=1000000, null=True)
    by_admin = models.BooleanField(default=False, null=True)


class Comment(models.Model):
    # This functionality is kind of a force for right now
    # replies = ArrayField(models.IntegerField(null=True), blank=True, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=1000000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now_add=True, null=True)
    by_admin = models.BooleanField(default=False, null=True)

    def create_comment(self, **kwargs):
        """
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db) # force_insert may need to be false
        return obj

    # Get method that returns comment object

    def get_comment(self):
        return self

    # Set methods

    def set_comment_user_id(self, new_user_id):
        self.user_id = new_user_id
        return self

    def set_comment_content(self, new_content):
        self.content = new_content
        return self

    def set_comment_date_created(self, new_date: str):
        """

        :param new_date: Must be of form (YYYY-MM-DD)
        :return: Updated Comment
        """
        formatted = models.DateTimeField(new_date)
        self.date_created = formatted
        return self

    def set_comment_date_modified(self, new_date: str):
        """

        :param new_date: Must be of form (YYYY-MM-DD)
        :return: Updated Comment
        """
        formatted = models.DateTimeField(new_date)
        self.date_modified = formatted
        return self

    def set_comment_by_admin(self, by_adm: bool):
        self.by_admin = by_adm
        return self

    # Remove from DB

    def remove_comment(self):
        # Not sure how to check if the deletion occurred correctly...
        self.delete(keep_parents=True)


class CreditCard(models.Model):
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    card_num = models.CharField(max_length=16, null=True)
    cvv = models.CharField(max_length=3, null=True)
    holder_name = models.CharField(max_length=50, null=True)
    card_expiration = models.DateTimeField(max_length=25, null=True)
    currently_used = models.BooleanField(default=True, null=True)

    def create_cc(self, **kwargs):
        """
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj

    def get_cc(self):
        return self

    # Set Methods

    def set_cc_user_id(self, new_id):
        self.user_id = new_id
        return self

    def set_card_num(self, new_num):
        self.card_num = new_num
        return self

    def set_cvv(self, new_cvv):
        self.cvv = new_cvv
        return self

    def set_holder_name(self, new_name):
        self.holder_name = new_name
        return self

    def set_expiration(self, new_date: str):
        formatted = models.DateTimeField(new_date)
        self.card_expiration = formatted
        return self

    def set_cc_in_use(self, use):
        self.currently_used = use
        return self

    # Remove method
    def remove_cc(self):
        self.delete(keep_parents=True)


class Filter(models.Model):
    filter_id = models.IntegerField(null=True)

    def create_filter(self, **kwargs):
        """
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj

    def get_filter(self):
        return self

    # Set Methods
    def set_filter_id(self, new_id):
        self.filter_id = new_id
        return self

    # Remove Method

    def remove_filter(self):
        self.delete(keep_parents=True)


class Image(models.Model):
    filter_used = models.BooleanField(default=False, null=True)
    original_image = models.ImageField(null=True)
    filtered_versions = ArrayField(models.ImageField(null=True), blank=True, null=True)
    filters_used = ArrayField(models.IntegerField(null=True), blank=True, null=True)
    is_flagged = models.BooleanField(default=False, null=True)
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    by_admin = models.BooleanField(default=False, null=True)

    def create_image(self, **kwargs):
        """
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj

    def get_image(self):
        return self

    # Set Methods

    def set_filter_used(self, use: bool):
        self.filter_used = use
        return self

    def set_original_image(self, image):
        formatted = models.ImageField(image)
        self.original_image = formatted
        return self

    def set_filters_used(self, filters: list([int])):
        # Not sure if this is how you do this either
        self.filter_used = ArrayField(filters, blank=True, null=True)
        return self

    def set_image_flagged(self, flag):
        self.is_flagged = flag
        return self

    def set_image_user(self, user: Member):
        # Not sure if this is the correct parameter to update
        self.user_id = models.ForeignKey(user, on_delete=models.CASCADE, null=True)
        return self

    def set_image_post(self, post: Post):
        # Not sure if this is the correct parameter to update
        self.post_id = models.ForeignKey(post, on_delete=models.CASCADE, null=True)
        return self

    # Remove Methods

    def remove_image(self):
        self.delete(keep_parents=True)
