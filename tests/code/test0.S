.global _start; 

_start:
    addi t0, zero, 1;
    addi t1, zero, 2;
    add t2, t1, t0;
    sw t2, 0(s1);
    sw t1, 1(s1);
    sw t0, 2(s1);
    mret;
