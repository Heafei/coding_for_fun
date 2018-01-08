/** Documentation
 * 
 * 
 */
#ifndef _DEFINE_H_
#define _DEFINE_H_

#if !defined(TRUE) || !defined(FALSE)
#define TRUE (1==1)
#define FALSE (!TRUE)
#endif

#if !defined ABS
  #define  ABS(x) ((x)>0 ? (x) : -(x))
#endif

#if !defined MAX
  #define  MAX( x, y ) ( ((x) > (y)) ? (x) : (y) )
#endif

#if !defined MIN
  #define  MIN( x, y ) ( ((x) < (y)) ? (x) : (y) )
#endif

#endif