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

$content = 'remains one of its funders.[ref name="factasia-supporters"]Factasia, <a href="https://web.archive.org/web/20190701085944/https://www.factasia.org/our-supporters/">Our Supporters</a>, website, undated, accessed July 2019[/ref] Other supporters supply services to the tobacco industry.[ref name="factasia-supporters-abcd"/]</td>
<td><a href="http://localhost/stop//wiki/foundation-for-a-smoke-free-world">Foundation for a Smoke-Free World</a>
The Foundation for a Smoke-Free World describes itself as “an independent, private foundation formed and operated free from the control or influence of any third party” but is solely funded by <a href="http://localhost/stop//wiki/philip-morris-international-"> Philip Morris</a> (PMI). It was established in September 2017 and formally launched at the Global Tobacco and Nicotine Forum 2017 with a budget of $80m annually.';


$data = [
  [
    'its funders.', 
    'Other supporters', 
    'its funders. Other supporters', 
    '<ref name=factasia-supporters>Factasia, [https://web.archive.org/web/20190701085944/https://www.factasia.org/our-supporters/ Our Supporters], website, undated, accessed July 2019</ref>', 
    'factasia-supporters'
  ], 
  [
    'tobacco industry.', 
    '</td><td>', 
    'tobacco industry. </td><td>', 
    '<ref name=factasia-supporters/>', 
    'factasia-supporters'
  ]
];

// var_dump($content);

$c = 0;
$p_match = 0; // perfect match
$f_match = 0; // first word match
$e_match = 0; // end word match
$failed_count = 0; // end word match
while ($c < count($data)) {
  // var_dump($data[$c][3]);

  // check if original or duplicate
  // Check for self closing tag regex
  preg_match('/\/>/', $data[$c][3], $match);
  $isDuplicate = !!count($match);
  // var_dump("isDuplicate:".$isDuplicate);

  // Check for starting two words
  $start_pos = strpos($content, $data[$c][0]);

  // Check for ending two words
  $end_pos = strpos($content, $data[$c][1]);

  /***  Both starting and ending words are found  ***/
  if($start_pos !== false && $end_pos !== false) {
    $p_match++;

    // Add the length of the word to get where the word finishes
    $start_pos = $start_pos+strlen($data[$c][0]);

    // Break String just before ref tag
    $str1 = substr($content, 0, $start_pos);

    // Break string just after ref tag
    $str2 = substr($content, $end_pos, count($content));

    // convert <ref> into [ref]
    $ref = $data[$c][3];
    $ref = str_replace('<',"[", $ref);
    $ref = str_replace('>',"]", $ref);

    // Insert the refference
    $new_content = $str1 . $ref . $str2;

  } elseif ($start_pos !== false) {
    /***  start word is found  ***/
    $f_match++;

    var_dump($data[$c][3]);

    // Add the length of the word to get where the word finishes
    $start_pos = $start_pos + strlen($data[$c][0]);

    // Break String just before ref tag
    $str1 = substr($content, 0, $start_pos);

    // Check if the the ref is there within 10 characters
    $check_string = substr($content, $start_pos, $start_pos+10);

    preg_match('/\[ref/', $check_string, $match);
    $refExists = !!count($match);

    // Check if ref doesn not exists
    if(!$refExists) {
      var_dump("a");
      // then we can append it imediately after the start
      $str2 = substr($content, $start_pos, count($content));
    } else {
      // Find the length of the reference to determine the position we start the second substring

      if($isDuplicate) {
        // Duplicate Reference Regex
        $reg_patern = '/\[ref(.*)\/\]/';
      } else {
        // Original Reference Regex
        $reg_patern = '/^\[ref(.*)\[/ref\]$/';
      }

      preg_match($reg_patern, $check_string, $reference_match);

      var_dump($reference_match);

      if($reference_match) {
        $end_pos = $start_pos + strlen($match[0]);
        $str2 = substr($content, $end_pos, count($content));
      }
    }

    // convert <ref> into [ref]
    $ref = $data[$c][3];
    $ref = str_replace('<',"[", $ref);
    $ref = str_replace('>',"]", $ref);

    // Insert the refference
    $new_content = $str1 . $ref . $str2;

  } elseif ($end_pos !== false) {
    /***  End word is found  ***/
    $e_match++;



  } else {
    $failed_count++;
  }

  var_dump($new_content);

  // If start word not found use end word minus ref to determin the position



  // var_dump($start_pos);
  // var_dump($end_pos);


  // Split the string just before the opening ref and imediately after the closing ref

    // Position where to stop the first string

    // Position where to begin the second string

  // Append new ref inbetween the split string




  $c++;
}


echo "Total: ".$c."<br />";
echo "Perfect Match: ".$p_match."<br />";
echo "First Word Match: ".$f_match."<br />";
echo "End Word March: ".$e_match."<br />";
echo "Failed: ".$failed_count."<br />";



// Looping csv file
// $file = fopen(__DIR__."\\reference_words.csv","r");
// var_dump($file);
// $c = 0;
// $t = 0;
// $r = 0;
// $f = 0;

// $new_content = '';
// while (($data = fgetcsv($file)) !== FALSE)
// {   
//   if($c == 0 ) {
//     $c++;
//     continue;
//   }

//   $position = strpos($stripped_content, $data[0]);

//   if(!($position !== false)) {
//     $position = strpos($stripped_content, $data[1]);
//     $r++;
//     // var_dump('reverse');
//   }


//   if($position !== false){
//     // var_dump($position);
//     // $string1 = substr($stripped_content, $position, strlen($data[0]));
//     // var_dump($string1);
//     // var_dump("start: ".$position." end: ".strlen($data[0]) );
//     // $split_pos =  $position + strlen($data[0]);
//     // $split_content = str_split($stripped_content, $split_pos);
//     // $new_content = implode($split_content[0], $data[3], $split_content);
//     // var_dump($split_content);
//     $t++;
//   } else {
//     var_dump("Row:".$c." # ".$data[0]." # ".$data[1]);
//     $f++;
//   }

//   $c++;
// }

// echo "Total: ".$c."<br />";
// echo "Match: ".$t."<br />";
// echo "RMatch: ".$r."<br />";
// echo "Failed: ".$f."<br />";
// var_dump($new_content);
