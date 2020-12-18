

<style type="text/css" media="all">

/* Body Font face */
body {
	<?php if(of_get_option('bodyfontlink') != '' and of_get_option('bodyfontface') != '') { ?>

  	<?php echo of_get_option('bodyfontface');?>

  	<?php } ?>;
   }

   h1.textlogo {
   	<?php if(of_get_option('logofontlink') != '' and of_get_option('logofontface') != '') { ?>

  	<?php echo of_get_option('logofontface');?>

  	<?php } ?>;
}

/* Headings Font face */
h1,h2,h3,h4,h5,h6, .main h1, #intro {
	<?php if(of_get_option('headingfontlink') != '' and of_get_option('headingfontface') != '') { ?>

	<?php echo of_get_option('headingfontface');?>

	<?php } ?>;
   }

</style>