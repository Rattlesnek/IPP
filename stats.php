<?php
/**********************************************************************

  FileName    [stats.php]

  SystemName  [IPP - Interpreter]

  PackageName [Statistics class]

  Author      [Adam Pankuch]

  Login       [xpanku00]

  Date        [5/3/2019]

***********************************************************************/

////////////////////////////////////////////////////////////////////////
///                             CLASSES                              ///
////////////////////////////////////////////////////////////////////////

/**
 * Class wrapping all statistics about parsed source code
 */
class Stats {
    private $select;            // array which contains order of output string
    private $loc;               // counter of lines of code
    private $comments;          // counter of comments
    private $labels;            // counter of labels
    private $specific_labels;   // array containing specific labels
    private $jumps;             // counter of jump instructions

    public function __construct($select, $loc=0, $comments=0, $labels=0, $jumps=0) {
        $this->select = $select;
        $this->loc = $loc;
        $this->comments = $comments;
        $this->labels = $labels;
        $this->specific_labels = array();
        $this->jumps = $jumps;
    }

    /**
     * Method increments number of comments
     */
    public function incComments() {
        $this->comments++;
    }

    /**
     * Method increments loc, jump, label counter based on opcode
     * @param $instruct     opcode of instruction
     */
    public function incInstructs($instruct, $operands) {
        $this->loc++;
        
        if ($instruct == 'LABEL' and ! empty($operands)) {
            if (! in_array($operands[0], $this->specific_labels)) {
                array_push($this->specific_labels, $operands[0]);
                $this->labels++;  
            }
        } elseif (strpos($instruct, 'JUMP') !== false) {
            $this->jumps++;
        }
    }

    /**
     * Method returns string of statistics based on selected statistics in select
     * @return string of statistics
     */
    public function str() {
        $string = '';
        foreach ($this->select as $sel) {
            if ('loc' == $sel)
                $string .= "$this->loc\n";
            elseif ('comments' == $sel)
                $string .= "$this->comments\n";
            elseif ('labels' == $sel)
                $string .= "$this->labels\n";
            elseif ('jumps' == $sel)
                $string .= "$this->jumps\n";
        }
        return $string;
    }

    /**
     * Getter function of attributes
     */
    public function __get($attr) {
        if (property_exists($this, $attr))
            return $this->$attr;
    }
}

?>