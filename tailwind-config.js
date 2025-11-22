     tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        display: ['Outfit', 'sans-serif'],
                    },
                    colors: {
                        brand: {
                            50: '#f0fdfa',
                            100: '#ccfbf1',
                            500: '#6366f1', // Indigo Primary
                            600: '#4f46e5',
                            700: '#4338ca',
                            900: '#312e81',
                            accent: '#0ea5e9',
                        }
                    },
                    animation: {
                        'scroll': 'scroll 40s linear infinite',
                        'float': 'float 6s ease-in-out infinite',
                        'aurora': 'aurora 10s infinite alternate',
                        'shimmer': 'shimmer 2s linear infinite',
                    },
                    keyframes: {
                        scroll: {
                            '0%': { transform: 'translateX(0)' },
                            '100%': { transform: 'translateX(-100%)' },
                        },
                        float: {
                            '0%, 100%': { transform: 'translateY(0)' },
                            '50%': { transform: 'translateY(-20px)' },
                        },
                        aurora: {
                            '0%': { transform: 'translate(0, 0) rotate(0deg) scale(1)' },
                            '100%': { transform: 'translate(20px, -20px) rotate(5deg) scale(1.1)' },
                        },
                        shimmer: {
                            'from': { backgroundPosition: '0 0' },
                            'to': { backgroundPosition: '-200% 0' },
                        }
                    }
                }
            }
        }