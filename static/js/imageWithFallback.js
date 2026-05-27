/**
 * ImageWithFallback Component
 * Gracefully handles image loading failures with a fallback placeholder
 * Can be used in future React integration or standalone
 */

const ERROR_IMG_SRC =
  'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODgiIGhlaWdodD0iODgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgc3Ryb2tlPSIjMDAwIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBvcGFjaXR5PSIuMyIgZmlsbD0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIzLjciPjxyZWN0IHg9IjE2IiB5PSIxNiIgd2lkdGg9IjU2IiBoZWlnaHQ9IjU2IiByeD0iNiIvPjxwYXRoIGQ9Im0xNiA1OCAxNi0xOCAzMiAzMiIvPjxjaXJjbGUgY3g9IjUzIiBjeT0iMzUiIHI9IjciLz48L3N2Zz4KCg=='

/**
 * ImageWithFallback - Vanilla JavaScript implementation
 * 
 * Usage:
 * const img = new ImageWithFallback({
 *   src: 'https://example.com/image.jpg',
 *   alt: 'Example image',
 *   className: 'w-full h-auto',
 *   onError: () => console.log('Image failed to load')
 * });
 */
export class ImageWithFallback {
  constructor(props = {}) {
    this.src = props.src;
    this.alt = props.alt || 'Image';
    this.className = props.className || '';
    this.style = props.style || {};
    this.onError = props.onError || null;
    this.didError = false;
    this.element = null;
    
    this.init();
  }

  init() {
    this.element = this.createImageElement();
  }

  createImageElement() {
    const img = document.createElement('img');
    img.src = this.src;
    img.alt = this.alt;
    img.className = this.className;
    
    // Apply inline styles
    Object.assign(img.style, this.style);
    
    // Handle error
    img.addEventListener('error', () => this.handleImageError());
    
    return img;
  }

  handleImageError() {
    if (this.didError) return;
    this.didError = true;
    
    // Create fallback container
    const container = document.createElement('div');
    container.className = `inline-block bg-gray-100 text-center align-middle ${this.className}`;
    Object.assign(container.style, this.style);
    
    // Create error image
    const errorImg = document.createElement('img');
    errorImg.src = ERROR_IMG_SRC;
    errorImg.alt = 'Error loading image';
    errorImg.dataset.originalUrl = this.src;
    
    // Create wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'flex items-center justify-center w-full h-full';
    wrapper.appendChild(errorImg);
    
    container.appendChild(wrapper);
    
    // Replace element
    if (this.element.parentNode) {
      this.element.parentNode.replaceChild(container, this.element);
    }
    this.element = container;
    
    // Call callback
    if (this.onError) {
      this.onError();
    }
  }

  getElement() {
    return this.element;
  }

  mount(selector) {
    const container = document.querySelector(selector);
    if (container) {
      container.appendChild(this.element);
    }
    return this;
  }

  appendTo(element) {
    element.appendChild(this.element);
    return this;
  }
}

/**
 * React Component Version (for future integration)
 * 
 * Usage in React:
 * import { ImageWithFallback } from './utils/ImageWithFallback'
 * 
 * function App() {
 *   return (
 *     <ImageWithFallback 
 *       src="https://example.com/image.jpg"
 *       alt="Example"
 *       className="w-full h-auto"
 *     />
 *   );
 * }
 */

// React version for future use
export function ImageWithFallbackReact(props) {
  const [didError, setDidError] = React.useState(false);

  const handleError = () => {
    setDidError(true);
  };

  const { src, alt, style, className, ...rest } = props;

  return didError ? (
    <div
      className={`inline-block bg-gray-100 text-center align-middle ${className ?? ''}`}
      style={style}
    >
      <div className="flex items-center justify-center w-full h-full">
        <img src={ERROR_IMG_SRC} alt="Error loading image" {...rest} data-original-url={src} />
      </div>
    </div>
  ) : (
    <img src={src} alt={alt} className={className} style={style} {...rest} onError={handleError} />
  );
}

export default ImageWithFallback;
