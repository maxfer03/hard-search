export default function useUtils() {
  const formatPrice = (raw, append='$') => {
    return (append || '') + Number(raw.toFixed(2)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }
  
  return { formatPrice }
}
