<?php
/*
The comments page for Site5 Framework
*/

// Do not delete these lines
  if (!empty($_SERVER['SCRIPT_FILENAME']) && 'comments.php' == basename($_SERVER['SCRIPT_FILENAME']))
    die ('Please do not load this page directly. Thanks!');

  if ( post_password_required() ) { ?>
  	<div class="help">
    	<p class="nocomments"><?php _e('This post is password protected. Enter the password to view comments.','site5framework'); ?></p>
  	</div>
  <?php
    return;
  }
?>

<!-- You can start editing here. -->

<?php if ( have_comments() ) : ?>

	<div id="comments">
		<h3><?php comments_number('<span>No</span> Comments', '<span>One</span> Comment', '<span>%</span> Comments' );?></h3>
		<ul class="commentlist">
			<?php wp_list_comments('type=comment&callback=site5framework_comments'); ?>
		</ul>
	</div>

	<?php else : // this is displayed if there are no comments so far ?>

	<?php if ( comments_open() ) : ?>
    	<!-- If comments are open, but there are no comments. -->

	<?php else : // comments are closed ?>
	<!-- If comments are closed. -->
	<p class="nocomments"><?php _e('Comments are closed.','site5framework'); ?></p>

	<?php endif; ?>

<?php endif; ?>


<?php if ( comments_open() ) : ?>

<section id="respond" class="respond-form">

	<div id="comment-form-title"><h3><?php _e( 'Post a comment', 'site5framework' ); ?></h3></div>

	<div id="cancel-comment-reply">
		<p class="small"><?php cancel_comment_reply_link(); ?></p>
	</div>

	<?php if ( get_option('comment_registration') && !is_user_logged_in() ) : ?>
  	<div class="help">
  		<p><?php _e("You must be  ", "site5framework"); ?> <a href="<?php echo wp_login_url( get_permalink() ); ?>"><?php _e("logged in ", "site5framework"); ?></a> <?php _e("to post a comment. ", "site5framework"); ?></p>
  	</div>
	<?php else : ?>

	<form action="<?php echo get_option('siteurl'); ?>/wp-comments-post.php" method="post" id="commentform">

	<ul id="comment-form-elements">

	<?php if ( is_user_logged_in() ) : ?>

	<li class="comments-logged-in-as"><?php _e("Logged in as  ", "site5framework"); ?><a href="<?php echo get_option('siteurl'); ?>/wp-admin/profile.php"><?php echo $user_identity; ?></a>. <a href="<?php echo wp_logout_url(get_permalink()); ?>" title="Log out of this account"><?php _e("Log out &raquo; ", "site5framework"); ?></a></li>


	<?php else : ?>

		<li>
		  <label for="author"><?php _e("Your Name*:", "site5framework"); ?></label>
		  <input type="text" name="author" id="author" value="<?php echo esc_attr($comment_author); ?>" tabindex="1" <?php if ($req) echo "aria-required='true'"; ?> />
		</li>

		<li>
		  <label for="email"><?php _e("Your Mail*:", "site5framework"); ?></label>
		  <input type="email" name="email" id="email" value="<?php echo esc_attr($comment_author_email); ?>" tabindex="2" <?php if ($req) echo "aria-required='true'"; ?> />
		</li>

		<li>
		  <label for="url"><?php _e("Your Website*:", "site5framework"); ?></label>
		  <input type="url" name="url" id="url" value="<?php echo esc_attr($comment_author_url); ?>" tabindex="3" />
		</li>

	<?php endif; ?>

		<li>
			<label for="comment"><?php _e("Your comment*: ", "site5framework"); ?></label>
			<textarea name="comment" id="comment" tabindex="4" rows="7" cols="100%"></textarea>
		</li>


	  <input name="submit" type="submit" id="submitcomment" class="submitbutton" tabindex="5"  value="<?php _e("POST COMMENT", "site5framework"); ?>" />
	  <?php comment_id_fields(); ?>

	<?php do_action('comment_form', $post->ID); ?>
	</ul>
	</form>

	<?php endif; // If registration required and not logged in ?>
</section>

<?php endif; // if you delete this the sky will fall on your head ?>
