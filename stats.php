<?php

class Stats {
    private $loc;
    private $comments;
    private $labels;
    private $jumps;

    public function __construct($loc=0, $comments=0, $labels=0, $jumps=0) {
        $this->loc = $loc;
        $this->comments = $comments;
        $this->labels = $labels;
        $this->jumps = $jumps;
    }

    public function incComments() {
        $this->comments++;
    }

    public function incInstructs($instruct) {
        $this->loc++;

        if ($instruct == 'LABEL')      
            $this->labels++;
        elseif (strpos($instruct, 'JUMP') !== FALSE)
            $this->jumps++;
    }

    public function str() {
        return  "loc:\t$this->loc\n" .
                "comms:\t$this->comments\n" .
                "labels:\t$this->labels\n" .
                "jumps:\t$this->jumps\n";
    }

    public function __get($attr) {
        if (property_exists($this, $attr))
            return $this->$attr;
    }
}

class XMLcreator {
    private $ins_cnt;
    private $DOM;

    public function __construct() {
        $this->ins_cnt = 0;
        $this->DOM = new DOMDocument('1.0', 'UTF-8');
        $this->DOM->formatOutput = true;
        $progXML = $this->DOM->createElement('program');
        $progXML->setAttribute('language', 'IPPcode19');
        $this->DOM->appendChild($progXML);
    }
}

?>