<?php
  $page_title = 'home';
  $dir_info = './';
  include_once('./header.php');
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

            <div class="hero-unit" style="vertical-align: middle;">
                <div class="row-fluid">
                    <div class="span6">
                        <h2>Welcome!</h2>
                        <p>
                            We're a group of students and professors tackling problems related to Folkman
                            numbers, a topic closely related to Ramsey theory and the study of Ramsey numbers.
                            Led by <a href="http://www.cs.rit.edu/~spr" target="_blank">Dr. Stanis&#322;aw Radziszowski</a>, 
                            the leading expert on Ramsey numbers, we are investigating computational techniques
                            to find exact values of Folkman numbers (where possible), and narrowing the bounds
                            where we can. 
                        </p>
                    </div>
                    <div class="span5">
                        <table style="width: 100%;">
                          <tr>
                             <td style="text-align: center; vertical-align: middle;">
                                  <img src="img/FolkmanLargeColor.png"/>
                             </td>
                          </tr>
                        </table>
                    </div>
                </div>
            </div>

            <div class="row-fluid">
                <div class="span12">
                    <!-- Example row of columns -->
                    <div class="span10 offset 1">
                        <p>
                        Folkman numbers, first introduced by Folkman in 1970 \cite{Folkman}, are concerned
                        with the graphs in which a monochromatic copy of a particular subgraph exists for all edge colorings. 
                        We write $G \to (a_1, ..., a_k; p)^e$ iff for every edge coloring of an undirected simple graph $G$ not 
                        containing $K_p$, there exists a monochromatic $K_{a_{i}}$ in color $i$ for some $i \in \{1, ..., k\}$. 
                        The edge Folkman number is defined as $F_e(a_1, ..., a_k) = \min\{|V(G)| : G \to (a_1, ..., a_k; p)^e\}$.
                        Similarly, the vertex Folkman number is defined as $F_v(a_1, ..., a_k) = \min\{|V(G)| : G \to (a_1, ..., a_k; p)^v\}$.
                        In 1970 Folkman proved that for all $k > \max(s,t)$, edge- and vertex- Folkman numbers $F_e(s,t;k$
                        and $F_v(s,t;k)$ exist. Prior to this, Erd\H{o}s and Hajnal posed the problem of finding $F_e(3,3;4)$, which
                        can be equivalently stated as the following question \cite{Erdos01}: 
                        </p>
                    </div>
                    <hr>
                </div>
            </div>
<?php include_once('./footer.php'); ?>