<?php
$postid = $post->ID;
?>
<div class="postmeta">
	<div class="icon audio"></div>
<?php get_template_part( 'content', 'meta' ); ?>
</div>
<h2><?php the_title();?></h2>
<div class="entry-content">
<?php if ( !is_singular() ) {
	 player_audio($postid);
	} else { 
	player_audio($postid);
	the_content();
	} ?>
<?php if(has_tag()){?>
<div class="tags"><?php the_tags('<strong>Tags:</strong> ', ', ', '<br />'); ?></div> 
<?php }?>
</div>