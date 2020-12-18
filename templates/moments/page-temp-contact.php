<?php
/*
Template Name: Contact
*/
if(isset($_POST['submitted'])) {
		//Check to make sure that the name field is not empty
		if(trim($_POST['contactName']) === '') {
			$nameError = __("You forgot to enter your name.", "site5framework");
			$hasError = true;
		} else {
			$name = trim($_POST['contactName']);
		}

		//Check to make sure sure that a valid email address is submitted
		if(trim($_POST['email']) === '')  {
			$emailError = __("You forgot to enter your email address.", "site5framework");
			$hasError = true;
		} else if (!eregi("^[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]{2,4}$", trim($_POST['email']))) {
			$emailError = __("You entered an invalid email address.", "site5framework");
			$hasError = true;
		} else {
			$email = trim($_POST['email']);
		}

		//Check to make sure message were entered
		if(trim($_POST['message']) === '') {
			$messageError = __("You forgot to enter your message.", "site5framework");
			$hasError = true;
		} else {
			if(function_exists('stripslashes')) {
				$message = stripslashes(trim($_POST['message']));
			} else {
				$message = trim($_POST['message']);
			}
		}

		//If there is no error, send the email
		if(!isset($hasError)) {
			$msg .= "------------User Info------------ \r\n"; //Title
			$msg .= "User IP: ".$_SERVER["REMOTE_ADDR"]."\r\n"; //Sender's IP
			$msg .= "Browser Info: ".$_SERVER["HTTP_USER_AGENT"]."\r\n"; //User agent
			$msg .= "Referrer: ".$_SERVER["HTTP_REFERER"]; //Referrer

			$emailTo = ''.of_get_option('veecard_contact_email').'';
			$subject = 'Contact Form Submission From '.$name;
			$body = "Name: $name \n\nEmail: $email \n\nMessage: $message \n\n $msg";
			$headers = 'From: '.$name.' <'.$email.'>' . "\r\n" . 'Reply-To: ' . $email;

			if(mail($emailTo, $subject, $body, $headers)) $emailSent = true;

	}

}
get_header();
?>

		<!-- featured article -->
        <div class="topbar"> </div>
     	<!-- featured article -->

	     	<!-- .main_content-->
	        <div class="main_content">

		        <!-- section content -->
		        <section class="content">

		        	<!-- standart article -->
				    <article <?php post_class(); ?>>

				    	<h2><span class="post_title_icon"></span><a href="<?php the_permalink();?>"><?php the_title();?></a></h2>

						<!-- entry-content -->
				        <div class="entry-content clearfix">
				        <div class="entry-colors"><div class="color_col_1"></div><div class="color_col_2"></div><div class="color_col_3"></div></div>


						<?php if (have_posts()) : while (have_posts()) : the_post(); ?>


						<?php
						if(is_search()){
							the_excerpt();
						}else{
						 the_content(__('Read More', 'site5framework'));
						}?>


					<?php endwhile; endif;?>

						<?php if(of_get_option('contact_map')!=''){?>
						<div id="contact-map">
							<?php echo of_get_option('contact_map') ?>
						</div>
						<?php }?>

						<p class="error" <?php if($hasError != '') echo 'style="display:block;"'; ?>>
							<i class="fa fa-exclamation-circle"></i> <?php _e('There was an error submitting the form.', 'site5framework'); ?>

						</p>

						<p class="thanks">
							<i class="fa fa-check-circle"></i> <?php _e('<strong>Thanks!</strong> Your email was successfully sent. We should be in touch soon.', 'site5framework'); ?>

						</p>

						<!-- contact form -->
						<form id="contactform" method="POST">

			                 <div class="form-row">
			                     <div class="input col_half first">
			                         <label for="name"><?php _e("Name", "site5framework"); ?><sup>*</sup></label>
			                         <input type="text" id="name" name="contactName" value="<?php if(isset($_POST['contactName'])) echo $_POST['contactName'];?>" class="requiredField"/>
							<span class="error" <?php if($nameError != '') echo 'style="display:block;"'; ?>><i class="fa fa-exclamation-circle"></i> <?php _e("You forgot to enter your name.", "site5framework");?></span>
			                     </div>
			                     <div class="input col_half">
			                         <label for="email"><?php _e("Email", "site5framework"); ?><sup>*</sup></label>
			                         <input type="text" id="email" name="email" value="<?php if(isset($_POST['email']))  echo $_POST['email'];?>" class="requiredField email"/>
							  <span class="error" <?php if($emailError != '') echo 'style="display:block;"'; ?>><i class="fa fa-exclamation-circle"></i> <?php _e("You forgot to enter your email address.", "site5framework");?></span>
			                     </div>
			                 </div>

			                 <div class="form-row">
			                     <div class="input textarea">
			                         <label for="message"><?php _e("Message", "site5framework"); ?><sup>*</sup></label>
			                         <textarea cols="20" rows="7" id="message" name="message" class="requiredField"><?php if(isset($_POST['message'])) { if(function_exists('stripslashes')) { echo stripslashes($_POST['message']); } else { echo $_POST['message']; } } ?></textarea>
							  <span class="error" <?php if($messageError != '') echo 'style="display:block;"'; ?>><i class="fa fa-exclamation-circle"></i> <?php _e("You forgot to enter your message.", "site5framework");?></span>
			                     </div>
			                 </div>

			                 <div class="form-row">
								<input type="hidden" name="submitted" id="submitted" value="true" />
								<input type="submit" value="<?php _e('Send', 'site5framework'); ?>" class="submitbutton" />
			                 </div>

			             </form>
			             <!-- end contact form -->

		             </div>
					 <!-- entry-content -->

				</article>
				<!-- standart article -->

			</section>
		    <!-- section content -->

		    <?php wp_reset_query(); ?>

			<?php get_sidebar(); ?>

	    </div>
        <!-- .main_content-->

<?php get_footer(); ?>


