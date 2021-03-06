<?php
  $page_title = 'log';
  $dir_info = '../';
  include_once('../header.php');
?>

        <div class="navbar">
            <div class="navbar-inner">
                <a class="brand" href="<?php echo $dir_info;?>">RIT Folkman Group</a>
                <ul class="nav">
                    <li><a href="<?php echo $dir_info;?>">Home</a></li>
                    <li><a href="<?php echo $dir_info;?>team">Team</a></li>
                    <li><a href="<?php echo $dir_info;?>publications">Publications</a></li>
                    <li class="active"><a href="<?php echo $dir_info;?>log">Research Log</a></li>
                </ul>
            </div>
        </div>

        <div class="container">
            <div class="tabbable tabs-left">
              <ul class="nav nav-tabs">
		<li><a href="#axj" data-toggle="tab">Appurv Jain</a></li>
                <li><a href="#arl" data-toggle="tab">Alexander Lange</a></li>
                <li class="active"><a href="#spr" data-toggle="tab">Stanis&#322;aw Radziszowski</a></li>
		<li><a href="#yqsun" data-toggle="tab">Yongqi Sun</a></li>
		<li><a href="#afw" data-toggle="tab">Alex Weinstock-Collins</a></li>
                <li><a href="#caw" data-toggle="tab">Christopher Wood</a></li>
              </ul>
              <div class="tab-content">
		<div class="tab-pane" id="axj">
		  <h3>Appurv Jain Log</h3>
		  <?php include_once('./axj.htm'); ?>
		</div>
                <div class="tab-pane" id="arl">
                  <h3>Alexander Lange Log</h3>
                  <?php include_once('./arl.htm'); ?>
                </div>
                <div class="tab-pane active" id="spr">
                  <h3>Stanis&#322;aw Radziszowski Log</h3>
                  <?php include_once('./spr.htm'); ?>
                </div>
		<div class="tab-pane" id="yqsun">
		  <h3>Yongqi Sun Log</h3>
		  <?php include_once('./yqsun.htm'); ?>
		</div>
		<div class="tab-pane" id="afw">
		  <h3>Alex Weinstock-Collins Log</h3>
		  <?php include_once('./afw.htm'); ?>
		</div>
                <div class="tab-pane" id="caw">
                  <h3>Christopher Wood Log</h3>
                  <?php include_once('./caw.htm'); ?>
                </div>
              </div>
            </div>
            
<?php include_once('../footer.php'); ?>
            
