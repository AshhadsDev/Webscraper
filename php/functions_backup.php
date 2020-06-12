<?php 



$my_postid = 2865;//This is page id or post id
$content_post = get_post($my_postid);
$content = get_the_content('more', false, $content_post);
// $content = $content_post->post_content;
// $content = apply_filters('the_content', $content);

// echo "<pre>";
// var_dump(substr($content, 1465, 1565));
// echo "</pre>";

// $string = 'While the IEA does not disclose its funding sources and has repeatedly received a “one star” (the lowest) rating by transparency watchdog Transparency International [ref ]Transparify, <a href="https://web.archive.org/web/20190103153936/https:/www.transparify.org/blog/2018/11/16/pressure-grows-on-uk-think-tanks-that-fail-to-disclose-their-funders">Pressure grows on UK think tanks that fail to disclose their funders</a>, 16 November 2018, accessed July 2019[/ref] it is known to have received funding from British American Tobacco (BAT) since 1963, and to date (January 2019) BAT describes itself as an IEA member in the EU Transparency Register.';

$string = 'remains one of its funders.[ref name="factasia-supporters"]Factasia, <a href="https://web.archive.org/web/20190701085944/https://www.factasia.org/our-supporters/">Our Supporters</a>, website, undated, accessed July 2019[/ref] Other supporters supply services to the tobacco industry.[ref name="factasia-supporters"]</td>
<td><a href="http://localhost/stop//wiki/foundation-for-a-smoke-free-world">Foundation for a Smoke-Free World</a>
The Foundation for a Smoke-Free World describes itself as “an independent, private foundation formed and operated free from the control or influence of any third party” but is solely funded by <a href="http://localhost/stop//wiki/philip-morris-international-"> Philip Morris</a> (PMI). It was established in September 2017 and formally launched at the Global Tobacco and Nicotine Forum 2017 with a budget of $80m annually.';
// var_dump($string);

// Removeing the origial references 
# $string_one = preg_replace("/\[ref.*?\](.*)?\[\/ref\]/","", $content); 
# $string_one = preg_replace("/^\[ref\]\[\/ref\]$/","", $content); 
$stripped_content = strip_ref_shortcodes($content);

// $string_one = preg_replace($reg,"", $content); 

// $tags_to_remove = apply_filters( 'strip_shortcodes_tagnames', 'ref', $content );
// var_dump($string_one);
// $string_one = strip_shortcodes($content); 

// Removeing the duplicate references 
// $string_two = preg_replace("/\[ref.*?\]/","", $string_one); 


// $test = strpos($stripped_content, 'Transparency International');
// $test2 = strpos($stripped_content, 'Transparency International  it is');
// $content = substr($stripped_content, 1465, 1565);
// var_dump($test);
// var_dump($test2);
// var_dump($test3);

// Looping csv file
$file = fopen(__DIR__."\\reference_words.csv","r");
var_dump($file);
$c = 0;
$t = 0;
$r = 0;
$f = 0;

$new_content = '';
while (($data = fgetcsv($file)) !== FALSE)
{   
  if($c == 0 ) {
    $c++;
    continue;
  }

  $position = strpos($stripped_content, $data[0]);

  if(!($position !== false)) {
    $position = strpos($stripped_content, $data[1]);
    $r++;
    // var_dump('reverse');
  }


  if($position !== false){
    // var_dump($position);
    // $string1 = substr($stripped_content, $position, strlen($data[0]));
    // var_dump($string1);
    // var_dump("start: ".$position." end: ".strlen($data[0]) );
    // $split_pos =  $position + strlen($data[0]);
    // $split_content = str_split($stripped_content, $split_pos);
    // $new_content = implode($split_content[0], $data[3], $split_content);
    // var_dump($split_content);
    $t++;
  } else {
    var_dump("Row:".$c." # ".$data[0]." # ".$data[1]);
    $f++;
  }

  $c++;
}

echo "Total: ".$c."<br />";
echo "Match: ".$t."<br />";
echo "RMatch: ".$r."<br />";
echo "Failed: ".$f."<br />";
// var_dump($new_content);

// Remove a specific shortcode 
// : copied from wp-includes\shortcodes.php
function strip_ref_shortcodes( $content ) {

    if ( false === strpos( $content, '[' ) ) {
        return $content;
    }
 
    // Find all registered tag names in $content.
    preg_match_all( '@\[([^<>&/\[\]\x00-\x20=]++)@', $content, $matches );
 
    $tags_to_remove = ['ref'];
 
    $tags_to_remove = apply_filters( 'strip_shortcodes_tagnames', $tags_to_remove, $content );
 
    $tagnames = array_intersect( $tags_to_remove, $matches[1] );
 
    if ( empty( $tagnames ) ) {
        return $content;
    }
 
    $content = do_shortcodes_in_html_tags( $content, true, $tagnames );
 
    $pattern = get_shortcode_regex( $tagnames );
    $content = preg_replace_callback( "/$pattern/", 'strip_shortcode_tag', $content );
 
    // Always restore square braces so we don't break things like <!--[if IE ]>.
    $content = unescape_invalid_shortcodes( $content );
 
    return $content;
}