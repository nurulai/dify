'use client'
import type { FC } from 'react'
import classNames from '@/utils/classnames'
import { useSelector } from '@/context/app-context'

type LogoSiteProps = {
  className?: string
}

const LogoSite: FC<LogoSiteProps> = ({
  className,
}) => {
  const { theme } = useSelector((s) => {
    return {
      theme: s.theme,
    }
  })

  const src = theme === 'light' ? '/logo/logo-site.png' : `/logo/logo-site-${theme}.png`
  return (
    <div className='flex items-center flex-row gap-2'>
      <img
        src={'/logo/bank-bjb-logo.png'}
        className={classNames('block w-auto h-8', className)}
        alt='logo'
      />
      <img
        src={src}
        className={classNames('block w-auto h-3', className)}
        alt='logo'
      />

      {/* <img
        src={'/logo/lintasarta-logo.png'}
        className={classNames('block w-auto h-10', className)}
        alt='logo'
      /> */}
    </div>
  )
}

export default LogoSite
