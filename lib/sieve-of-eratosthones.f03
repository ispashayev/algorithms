! Computes a set of prime numbers
!
! Takes in a command-line input (REQUIRED!). Parses this input as an integer
! and generates that number of prime numbers. This algorithm used the sieve
! of Eratosthenes to generate primes. Since the upper bound of candidate
! primes must be known beforehand, we use the Prime Number Theorem to
! approximate the upper bound (via Newton's Method). Consequently, this
! algorithm isn't guaranteed to return the exact number of requested primes.

program sieveOfEratosthenes
  implicit none

  ! Type declarations
  integer, pointer :: primes (:)
  integer :: num_primes, num_primes_found = 0
  character (20) :: num_primes_arg

  logical, pointer :: sieve (:) ! a dynamic array for the sieve of eratosthenes
  integer :: i, error, start, end
  integer :: base_prime = 2
  integer :: num_chunks = 1, chunk_size

  ! Read command-line argument specifying number of primes to compute
  call get_command_argument(1, num_primes_arg)
  read (num_primes_arg, fmt="(i20)") num_primes

  ! Approximate the chunk size for allocations using the Prime Number Theorem
  call pnt_approximation(num_primes, chunk_size)
  
  print *, "Interval size estimate using prime number theorem:", chunk_size
  
  ! Allocate the array and set the upper bound
  allocate(primes(num_primes), stat=error)
  if (error .ne. 0) then
    print *, "Unable to allocate memory for primes array."
    stop
  end if

  allocate(sieve(chunk_size), stat=error)
  if (error .ne. 0) then
    print *, "Unable to allocate memory for sieve of Eratosthenes."
    stop
  end if

  start = 1
  end = chunk_size
  sieve(start:end) = .true. ! initialize all array elements to true
  sieve(start) = .false. ! 1 is not a prime number

  do 20 i = base_prime, end
    if (sieve(i)) then
      num_primes_found = num_primes_found + 1
      primes(num_primes_found) = i
      sieve(2*i:end:i) = .false.
      if (num_primes_found == num_primes) then
        exit
      end if
    end if
  20 continue

  do 30 i = 1, num_primes_found
    print *, primes(i)
  30 continue

  print *, ""
  print *, "Total number of primes found:", num_primes_found

  deallocate(primes, stat=error)
  if (error .ne. 0) then
    print *, "Unable to free memory for primes array."
    stop
  end if

  deallocate(sieve, stat=error)
  if (error .ne. 0) then
    print *, "Unable to free memory for sieve of Eratosthenes."
    stop
  end if

end program sieveOfEratosthenes

! The following subroutine approximates an interval size  for containing
! NUM_PRIMES primes. The approximation is stored in INTERVAL_SIZE. The
! algorithm used for approximation is Newton's Method to solve the equation
! given by the Prime Number Theorem, i.e. the number of primes in the interval
! [0,x] is approximately x / ln(x) We set this value equal to NUM_PRIMES and
! solve for x, where x is equivalent to INTERVAL_SIZE. 
subroutine pnt_approximation(num_primes, interval_size)
  implicit none

  integer, intent(in) :: num_primes
  integer, intent(out) :: interval_size

  integer :: i
  real :: xt, prime_count_approx, dprime_count_approx

  xt = num_primes

  print *, "Approximating the interval size for", num_primes, "primes..."

  do 30 i = 0, 50
    prime_count_approx = xt / log(xt) - num_primes
    dprime_count_approx = (log(xt) - 1.0) / log(xt)**2
    xt = xt - prime_count_approx / dprime_count_approx
  30 continue

  print *, "Done."
  print *, ""

  interval_size = xt

end subroutine pnt_approximation
