<?php
$debug = false;
$file = 'php.spec';
// PHP 5.3.0
$extsubdir = 'php/extensions/no-debug-non-zts-20090626';

if (in_array('dbg', $argv)) {
    $debug = true;
    $extsubdir = 'php/extensions/debug-non-zts-20090626';
    $file = 'php-dbg.spec';
}

$in = file_get_contents('php.spec.in');

if ($debug) {
    $fr = array(
        '{:dbg}' => '-dbg',
        '{:dbgc}' => '',
        '{:dbgenable}' => '--enable-debug ',
        '{:extsubdir}' => $extsubdir,
    );
} else {
    $fr = array(
        '{:dbg}' => '',
        '{:dbgc}' => '-dbg',
        '{:dbgenable}' => '',
        '{:extsubdir}' => $extsubdir,
    );    
}

$find = array_keys($fr);
$replace = array_values($fr);

$out = str_replace($find, $replace, $in);

file_put_contents("../$file", $out);